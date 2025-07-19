import json
from typing import List, Optional
from langchain.tools import tool
from backend.services.employee_service import EmployeeService

@tool
def search_employees(
    job_titles: List[str] | None = None,
    skills: List[str] | None = None,
    department: str | None = None,
    availability: str | None = None,
    skill_search_mode: str = 'AND'
) -> str:
    """
    Searches the employee database.
    - 'job_titles': Finds employees matching ANY title (OR search).
    - 'skills': Finds employees matching skills based on 'skill_search_mode'.
    - 'skill_search_mode': Use 'AND' to find employees with ALL listed skills. Use 'OR' to find employees with ANY of the skills. Defaults to 'AND'.
    - 'department', 'availability' are filters.
    Returns a JSON string of matching profiles.
    """
    employee_service = EmployeeService()
    results = employee_service.search_employees(
        job_titles=job_titles,
        skills=skills,
        department=department,
        availability=availability,
        skill_search_mode=skill_search_mode
    )
    # Convert Employee objects to dictionaries for JSON serialization
    return json.dumps([emp.dict() for emp in results], indent=2)
