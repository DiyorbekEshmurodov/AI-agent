from pydantic import BaseModel, Field
from typing import List , Optional

class ResumeExtract(BaseModel):
    name: Optional[str] = Field(
        None, description="Candidate full name if present")
    summary: Optional[str] = Field(None, description="Short summary/profile")
    years_experience: Optional[float] = Field(
        None, description="EEstimated total years of experience")
    skills: List[str] = Field(default_factory=list,
                              description="Normalized skills list (lowercase)")
    education: Optional[str] = Field(
        None, description="Highest degree or main education summary")
    recent_companies: List[str] = Field(default_factory=list, description="Recent employers")
    project: List[str] = Field(default_factory=list, description="Short list or key projects")

class ScoreBreakdown(BaseModel):
    skill_match : int = Field(description="0-100 skill match score")
    experience_match : int = Field(description="0-100 experience match score")
    education_match: int = Field(description="0-100 education match score")
    overall : int = Field(description="0-100 overall score")

class HRDecision(BaseModel):
    decision:  str =  Field(description="PASS or REJECT")
    reasons : List[str] = Field(description="Concise reasons supporting the decision")
    improvements : List[str] = Field(
        description="Suggestions for candidate improvements")
    score: ScoreBreakdown