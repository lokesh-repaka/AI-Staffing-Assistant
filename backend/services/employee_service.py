import json
from typing import List, Optional, Dict, Any
from backend.core.database import get_db_connection
from backend.models.employee import Employee

class EmployeeService:
    def search_employees(
        self,
        job_titles: Optional[List[str]] = None,
        skills: Optional[List[str]] = None,
        department: Optional[str] = None,
        availability: Optional[str] = None,
        skill_search_mode: str = 'AND'
    ) -> List[Employee]:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM employees WHERE 1=1"
        params = []

        if job_titles:
            title_conditions = [f"LOWER(jobTitle) LIKE ?" for title in job_titles]
            query += f" AND ({' OR '.join(title_conditions)})"
            params.extend([f"%{title.lower()}%" for title in job_titles])

        if department:
            query += " AND LOWER(department) LIKE ?"
            params.append(f"%{department.lower()}%")

        if availability:
            query += " AND LOWER(availability) = ?"
            params.append(availability.lower())

        if skills:
            skill_queries = []
            skill_params = []
            for skill in skills:
                skill_queries.append(f"LOWER(skills) LIKE ?")
                skill_params.append(f'%"skill": "{skill.lower()}"%')

            if skill_search_mode.upper() == 'OR':
                query += f" AND ({' OR '.join(skill_queries)})"
                params.extend(skill_params)
            elif skill_search_mode.upper() == 'AND':
                query += f" AND ({' AND '.join(skill_queries)})"
                params.extend(skill_params)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()

        results = []
        for row in rows:
            employee_dict = dict(row)
            employee_dict['certifications'] = json.loads(employee_dict['certifications'])
            employee_dict['skills'] = json.loads(employee_dict['skills'])
            employee_dict['projectHistory'] = json.loads(employee_dict['projectHistory'])
            results.append(Employee(**employee_dict))
        return results
