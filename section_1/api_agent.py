from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from dotenv import load_dotenv
from langchain_core.tools import tool
load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-120b",temperature=1)

search_tools = DuckDuckGoSearchRun()
tools=[search_tools]

prompt = ChatPromptTemplate.from_messages([
    ("system","Sen yordamchi agentsan . React sifatida fikr yurit va kerak bulsa foydali vositalardan foydalan"),
    ("human","{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])
agent_runnable =  create_tool_calling_agent(llm=llm,tools=tools,prompt=prompt)
agent = AgentExecutor(agent=agent_runnable,tools=tools,verbose = True)

if __name__ == "__main__":
    out = agent.invoke(
        {"input":"O`zbekistondagi eng baland tog` qaysi? "}
    )
    print(out["output"])