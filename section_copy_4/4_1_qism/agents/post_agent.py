from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.4)

post_prompt = ChatPromptTemplate.from_messages([
    ("system","You are professional LinkedIn content creator specializing in technology."),
    ("human",
     "Write a clear, engaging LinkedIn post about this topic: \n {topic}")
])

post_chain = post_prompt | llm

def post_node(state):
    response = post_chain.invoke({"topic":state['topic']})
    return {"post_text":response.content}