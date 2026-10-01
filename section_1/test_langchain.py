import os
from dotenv import load_dotenv
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-120b",temperature=0)
response=llm.invoke([HumanMessage(content="Salom! AI agent nima?")])
print(response)