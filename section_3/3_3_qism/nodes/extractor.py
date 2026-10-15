from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from ..schemas import ResumeExtract

extract_prompts = ChatPromptTemplate.from_messages([
    ("system","You are an expert HR analyst.Extract info from the resume text"),
    ("human","Resume text:\n'''\n{resume_text}\n'''\n\n Return a structured summary with: name , summary years_experience"
    "(float if possible) , skills (list of normalized lowercase strings),education (short), recent_companies (list)"
     "project (list).")
])
_llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=1)

extractor_chain = extract_prompts | _llm.with_structured_output(ResumeExtract)

def extractor_node(state: Dict) -> Dict:
    """
    Input:
        state['resume_text'] -> text
    output:
        {"extracted": ResumeExtract}
    """
    extracted : ResumeExtract = extractor_chain.invoke({"resume_text": state["resume_text"]})
    return {"extracted": extracted}