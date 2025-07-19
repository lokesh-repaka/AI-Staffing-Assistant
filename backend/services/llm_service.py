import operator
import json
from typing import Annotated, List, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, AIMessage # Import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from backend.core.config import settings
from src.tools import search_employees, read_document

class AgentState(dict):
    messages: Annotated[List[BaseMessage], operator.add]

class LLMService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            google_api_key=settings.GOOGLE_API_KEY
        )
        self.tools = [search_employees, read_document]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.app = self._compile_graph()

    def _compile_graph(self):
        system_prompt = """
        You are a world-class AI Staffing Assistant. Your mission is to find the best person for a project using a strategic, multi-step search process.

        **Your Search and Analysis Procedure (MUST be followed):**

        **1. Initial Strict Search:**
           - First, identify all the key skills required from the user's request and any documents.
           - If the user mentions a file path (e.g., 'requirements.docx'), you MUST use the `read_document` tool to get its content before proceeding.
           - Perform a search using the `search_employees` tool with `skill_search_mode='AND'`. This is your attempt to find the "perfect" candidate who has every required skill.

        **2. Fallback Lenient Search (If necessary):**
           - **IF AND ONLY IF** your initial 'AND' search returns no results, you MUST perform a second, broader search.
           - For this second search, identify the 2-3 most critical skills and use the tool with `skill_search_mode='OR'`.
           - You are now looking for the "best fit" from a wider pool.

        **3. Holistic Analysis & Recommendation:**
           - Analyze the candidates returned from your successful search (either the 'AND' or the 'OR' search).
           - Compare their full profiles: skills proficiency, relevant project history, and experience.
           - Select the single best candidate.

        **4. Formulate the Final Answer:**
           - Present your final answer using the structured format below.
           

        **Final Answer Format:**

        **Recommendation:**
        [Name of the single best candidate and their Job Title]

        **Overall Justification:**
        [Detailed paragraph explaining WHY this person is the top choice. Explain your why the employee is best.]

        **Key Strengths:**
        - [Bulleted list of their most relevant skills and projects.]

        **Other Strong Candidates Considered:**
        - [Briefly mention 1-2 other candidates and why they were not the top pick.]
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        agent = prompt | self.llm_with_tools

        def agent_node(state: AgentState):
            result = agent.invoke(state)
            return {"messages": [result]}

        tool_node = ToolNode(self.tools)

        def should_continue(state: AgentState) -> str:
            last_message = state["messages"][-1]
            # Check if the last message is an AIMessage and if it has tool_calls
            if isinstance(last_message, AIMessage) and last_message.tool_calls:
                return "tools"
            return "end"

        graph = StateGraph(AgentState)
        graph.add_node("agent", agent_node)
        graph.add_node("tools", tool_node)
        graph.set_entry_point("agent")
        graph.add_conditional_edges(
            "agent", should_continue, {"tools": "tools", "end": END},
        )
        graph.add_edge("tools", "agent")
        return graph.compile()

    def process_query(self, query: Optional[str] = None, file_path: Optional[str] = None):
        full_query_content = query if query else ""
        if file_path:
            full_query_content += f"\n\n(Refer to document at: {file_path})"

        inputs = {"messages": [HumanMessage(content=full_query_content)]}
        
        final_response_content = ""
        for s in self.app.stream(inputs, stream_mode="values"):
            last_message = s["messages"][-1]
            # Only capture the final content from the agent
            if isinstance(last_message, AIMessage) and not last_message.tool_calls and last_message.content:
                final_response_content = last_message.content
        return final_response_content