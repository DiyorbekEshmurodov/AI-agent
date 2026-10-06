from pydantic import BaseModel, Field

class ResumeExtract(BaseModel):
    name: str
    summary: str
    years_experience: float
    skills: list[str]
    education: str
    recent_companies: list[str]
    project: list[str]