from fastapi import FastAPI
from backend.api.v1.endpoints import employees
from backend.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(employees.router, prefix=settings.API_V1_STR + "/employees", tags=["employees"])

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Staffing Assistant API"}
