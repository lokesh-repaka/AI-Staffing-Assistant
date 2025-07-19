# AI Staffing Assistant

The AI Staffing Assistant is a powerful tool designed to streamline the process of finding the best-suited employees for various projects. It leverages a FastAPI backend for robust API services, a Streamlit frontend for an intuitive user interface, and integrates with a Large Language Model (LLM) to provide intelligent staffing recommendations based on project requirements or uploaded documents.

## Problem Statement

**Problem:** Operations Managers face a significant challenge in efficiently finding and assigning the most suitable employee to a given project from across the entire company. The manual process of identifying talent is often time-consuming, limited to the manager's immediate network, and can result in sub-optimal skill-to-task matching. This inefficiency leads to project delays, underutilization of the company's full talent pool, and a reduced ability to respond quickly to new business requirements or unexpected disruptions.

## Solution

The proposed solution is an AI-powered Staffing Assistant designed to automate and optimize the employee selection process. The system leverages a Large Language Model (LLM) to function as an intelligent agent.

**Workflow:**
1.  **Inputs:** An Operations Manager initiates the process by providing two key pieces of information:
    *   A natural language query describing the project or task.
    *   A document (e.g., PDF, DOCX) containing detailed project requirements.
2.  **Data Integration:** The AI agent accesses a comprehensive knowledge base of employee data stored in SharePoint. This data includes employee skills, proficiencies, project history, and other relevant attributes.
3.  **AI Analysis:** The LLM (Azure GPT-4o) processes the manager's query, the project document, and the SharePoint employee data.
4.  **Matching & Recommendation:** The agent cross-references the project requirements with the skills and competencies of all available employees. It then identifies and suggests the best-suited employee(s), providing a match percentage to quantify the recommendation.
5.  **Output:** The final recommendation is presented to the manager in a clear, formatted output.

## Key Benefits

*   **Drastic Time Reduction:** Aims to achieve a 90% reduction in the time required to find the right talent.
*   **Company-Wide Talent Optimization:** Breaks down departmental silos by enabling a search across the entire organization's talent pool.
*   **Enhanced Agility:** Allows the company to staff projects and respond to disruptions more rapidly and effectively.

## Features

*   **Employee Search:** Efficiently search for employees based on job titles, skills (with 'AND'/'OR' modes), department, and availability.
*   **LLM-Powered Recommendations:** Get intelligent staffing recommendations by providing natural language queries or uploading project requirement documents. The LLM analyzes the requirements and suggests the best-fit candidate(s).
*   **Document Processing:** Supports reading and extracting information from PDF, DOCX, and TXT files for comprehensive requirement analysis.
*   **Scalable Backend:** Built with FastAPI, providing a high-performance and easy-to-use API.
*   **Interactive Frontend:** A user-friendly interface developed with Streamlit for seamless interaction.
*   **SQLite Database:** Simple and efficient data storage for employee profiles.

## Technologies Used

*   **Backend:** Python 3.9+, FastAPI, Uvicorn, LangChain, LangGraph, Google Gemini API
*   **Frontend:** Python 3.9+, Streamlit, Requests
*   **Database:** SQLite
*   **Document Processing:** PyPDF2, python-docx
*   **Dependency Management:** `pip`

## Setup and Installation

Follow these steps to get the AI Staffing Assistant up and running on your local machine.

### Prerequisites

*   Python 3.9+ installed.
*   A Google API Key for accessing the Gemini LLM.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-staffing-assistant.git
cd ai-staffing-assistant
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

*   **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```
*   **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```

### 4. Install Dependencies

Install all required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 5. Set up Environment Variables

Create a `.env` file in the root directory of the project (e.g., `ai-staffing-assistant/.env`) and add your Google API Key:

```
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
```

Replace `"YOUR_GEMINI_API_KEY"` with your actual Google API Key.

### 6. Initialize the Database

The project uses an SQLite database (`employees.db`) populated from `employees.json`. Run the setup script to create and populate the database:

```bash
python scripts/setup_database.py
```

This will create `employees.db` in the project root and fill it with sample employee data.

## Running the Application

The application consists of two main parts: the Backend API and the Frontend Streamlit App.

### 1. Start the Backend API

Navigate to the project root directory and run the FastAPI application using Uvicorn:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be accessible at `http://localhost:8000`. The `--reload` flag will automatically restart the server on code changes.

### 2. Start the Frontend Streamlit App

Open a new terminal window (and activate your virtual environment if you closed the previous one) and run the Streamlit application:

```bash
streamlit run frontend/app.py
```

This will open the Streamlit application in your web browser, usually at `http://localhost:8501`.

## API Endpoints

The backend API exposes the following key endpoints:

*   **`/api/v1/employees/search` (POST)**
    *   **Description:** Searches for employees based on various criteria.
    *   **Request Body:** `EmployeeSearch` model (JSON)
    *   **Response:** List of `Employee` objects.
*   **`/api/v1/employees/llm_query` (POST)**
    *   **Description:** Processes a natural language query or an uploaded document to get LLM-powered staffing recommendations.
    *   **Request Body:** `query` (string, optional) and/or `file` (file upload, optional).
    *   **Response:** `LLMResponse` object containing the recommendation.

## Project Structure

```
.
├── backend/                  # FastAPI backend application
│   ├── api/                  # API endpoints
│   │   └── v1/
│   │       └── endpoints/
│   │           └── employees.py  # Employee search and LLM query endpoints
│   ├── core/                 # Core configurations (settings, database)
│   ├── models/               # Pydantic models for data validation
│   ├── services/             # Business logic for employee and LLM operations
│   └── main.py               # Main FastAPI application entry point
├── frontend/                 # Streamlit frontend application
│   └── app.py                # Main Streamlit app
├── scripts/                  # Utility scripts
│   └── setup_database.py     # Script to initialize the SQLite database
├── src/                      # Source code for tools and utilities
│   └── tools/                # LangChain tools for LLM
│       ├── document_reader.py  # Tool to read documents
│       └── employee_search_tool.py # Tool to search employees
├── employees.json            # Sample employee data
├── employees.db              # SQLite database (generated after setup)
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables file
└── README.md                 # Project README
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
