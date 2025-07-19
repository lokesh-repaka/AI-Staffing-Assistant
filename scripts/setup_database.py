import sqlite3
import json
import os
from backend.core.config import settings

# Define the file paths
json_file = 'employees.json'
db_file = settings.DATABASE_PATH

# Optional: Remove old database file if it exists to start fresh
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Removed old database file: {db_file}")

# --- Load Data from JSON File ---
with open(json_file, 'r') as f:
    employee_data = json.load(f)
    print(f"Loaded {len(employee_data)} records from {json_file}")

# --- Connect to SQLite Database and Get Cursor ---
# This will create the database file if it doesn't exist
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# --- Create the 'employees' Table ---
# Use "IF NOT EXISTS" to make the script re-runnable
# Store complex fields (lists/dicts) as TEXT by converting them to JSON strings
create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
    employeeId TEXT PRIMARY KEY,
    name TEXT,
    jobTitle TEXT,
    department TEXT,
    email TEXT,
    yearsOfExperience INTEGER,
    availability TEXT,
    manager TEXT,
    location TEXT,
    certifications TEXT,
    skills TEXT,
    projectHistory TEXT
);
"""
cursor.execute(create_table_query)
print("Table 'employees' created or already exists.")

# --- Insert Data into the Table ---
insert_count = 0
for employee in employee_data:
    # Use "INSERT OR REPLACE" to handle re-running the script. It will update records if the employeeId already exists.
    insert_query = """
    INSERT OR REPLACE INTO employees (
        employeeId, name, jobTitle, department, email, yearsOfExperience,
        availability, manager, location, certifications, skills, projectHistory
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    # Convert lists and dicts to JSON strings for storage
    data_tuple = (
        employee.get('employeeId'),
        employee.get('name'),
        employee.get('jobTitle'),
        employee.get('department'),
        employee.get('email'),
        employee.get('yearsOfExperience'),
        employee.get('availability'),
        employee.get('manager'),
        employee.get('location'),
        json.dumps(employee.get('certifications', [])),
        json.dumps(employee.get('skills', [])),
        json.dumps(employee.get('projectHistory', []))
    )
    cursor.execute(insert_query, data_tuple)
    insert_count += 1

# --- Commit Changes and Close Connection ---
conn.commit()
conn.close()

print(f"--- Process Complete ---")
print(f"Successfully inserted/updated {insert_count} records into '{db_file}'.")
print("Your database is now ready!")