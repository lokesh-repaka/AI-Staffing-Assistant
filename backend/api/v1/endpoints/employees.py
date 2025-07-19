from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from backend.models.employee import Employee, EmployeeSearch
from backend.services.employee_service import EmployeeService
from backend.models.llm import LLMQuery, LLMResponse
from backend.services.llm_service import LLMService
import os

router = APIRouter()

@router.post("/search", response_model=List[Employee])
async def search_employees_api(
    search_params: EmployeeSearch,
    employee_service: EmployeeService = Depends()
):
    try:
        employees = employee_service.search_employees(
            job_titles=search_params.job_titles,
            skills=search_params.skills,
            department=search_params.department,
            availability=search_params.availability,
            skill_search_mode=search_params.skill_search_mode
        )
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/llm_query", response_model=LLMResponse)
async def llm_query_api(
    query: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    llm_service: LLMService = Depends()
):
    file_path = None
    if file:
        try:
            # Ensure the 'temp' directory exists
            os.makedirs("temp", exist_ok=True)
            file_path = os.path.join("temp", file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")

    if not query and not file_path:
        raise HTTPException(status_code=400, detail="Either 'query' or 'file' must be provided.")

    try:
        response = llm_service.process_query(query=query, file_path=file_path)
        return LLMResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path) # Clean up the uploaded file