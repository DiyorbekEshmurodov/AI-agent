from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from ..schemas import ResumeExtract , HRDecision

score_system = "You are HR screening assistant . Compare the candidate`s resume against teh job requirements. Be"
"strict but fair . Score each area (skills/experience/education) on 0-100. Decide PASS  only if overall >= threshold"
"and must-have skills are sufficiently met."

score_prompt = ChatPromptTemplate.from_messages([
    ("system", score_system),
    ("human","Job description: \n'''\n{job_description}\n}'''\n\n Minimum years of experience: {min_years}\n must-have"
    "skills: {must_have_skills}\n Nice-to=have skills : {nice_to_have_skills}\n Pass threshold (overall score): {threshold}\n\n"
    "Extracted resume (JSON): \n{extracted_json}\n\nReturn PASS or REJECT with reasons , improvements, ans detailed score breakdown")
])

_llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=1)

scorer_chain = score_prompt | _llm.with_structured_output(HRDecision)

def score_node(state: Dict) -> Dict:
    extracted : ResumeExtract = state["extracted"]
    threshold : int = state.get("threshold",70)

    result: HRDecision = scorer_chain.invoke({
        "job_description": state['job_description'],
        "min_years": state['min_years'],
        "must_have_skills": state['must_have_skills'],
        "nice_to_have_skills": state['nice_to_have_skills'],
        "threshold": threshold,
        "extracted_json": extracted.model_dump_json(indent=2),
    })
    return {
        "decision" : result.decision,
        "reasons": result.reasons,
        "improvements": result.improvements,
        "score" : result.score.model_dump()
    }