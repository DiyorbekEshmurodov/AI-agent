from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.4)

post_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional LinkedIn content create specializing in technology"),
    ("human", "Write a clear , Engaging LinkedIn post about the topic: \n {topic}")
])

post_chain = post_prompt | llm

def post_node(state):
    response = post_chain.invoke({"topic": state['topic']})
    return {"post_text":response.content}