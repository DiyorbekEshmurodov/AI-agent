from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import AgentExecutor , create_tool_calling_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-120b",temperature=1)

search_tools = DuckDuckGoSearchRun()
@tool
def multiply(a:int,b:int):
    """Ikki sonni bir- biriga kupaytiruvchi fuksiya."""
    return a*b

tools = [search_tools , multiply]

prompt = ChatPromptTemplate.from_messages([
    ("system","Sen yordamchi agentsan. React sifatida fikir yurit va kerak bulsa foydali vositalardan foydalan"),
    ("human","{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

agent_runnable = create_tool_calling_agent(llm=llm,tools=tools,prompt=prompt)
agent = AgentExecutor(agent=agent_runnable,tools=tools,verbose=True)

if __name__ == "__main__":
    out = agent.invoke(
        {"input": "Meni ismim Sherale "}
    )
    print(out["output"])
    out = agent.invoke(
        {"input": "O`zbekistondagi poytaxti qayer? "}
    )
    print(out["output"])

    out = agent.invoke(
        {"input": "5 kupaytirsa 10 nima qanday javob chiqadi"}
    )
    print(out["output"])
    out = agent.invoke(
        {"input": "Meni ismim nima?"}
    )
    print(out["output"])