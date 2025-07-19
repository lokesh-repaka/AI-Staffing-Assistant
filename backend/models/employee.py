from pydantic import BaseModel, Field
from typing import List, Optional

class Skill(BaseModel):
    skill: str
    proficiency: str

class ProjectHistory(BaseModel):
    projectName: str
    description: str

class Employee(BaseModel):
    employeeId: str
    name: str
    jobTitle: str
    department: str
    email: str
    yearsOfExperience: int
    availability: str
    manager: str
    location: str
    certifications: List[str]
    skills: List[Skill]
    projectHistory: List[ProjectHistory]

class EmployeeSearch(BaseModel):
    job_titles: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    department: Optional[str] = None
    availability: Optional[str] = None
    skill_search_mode: Optional[str] = 'AND'
