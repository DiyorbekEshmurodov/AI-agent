import os
from typing import Dict
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel , Field
from langchain_groq import ChatGroq
load_dotenv()

class WriterOutput(BaseModel):
    code: str = Field(description="Generate Python code")
    explanation : str = Field(description="Explanation of what the code does")
llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=1)

writer_prompt = ChatPromptTemplate.from_messages([
    ("system","You are Python coding assistant. Generate clean , correct code."),
    ("human", "Write Python code following task: \n{task}\n The explain what the code does."),
    # MessagesPlaceholder("agent_scratchpad"),
])

writer_chain=writer_prompt | llm.with_structured_output(WriterOutput)

def writer_node(state):
    result: WriterOutput = writer_chain.invoke({"task":state['task']})
    return {"code": result.code , "explanation": result.explanation}

