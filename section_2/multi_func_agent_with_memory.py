from typing import Dict
from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=1)

search_tools = DuckDuckGoSearchRun()


@tool
def multiply(a: int, b: int):
  """Ikkita sonni bir-biriga ko'paytiruvchi funksiya."""
  return a * b


tools = [search_tools, multiply]

# 1. Prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "Sen yordamchi agentsan . React sifatida fikr yurit va kerak bulsa"
            " foydali vositalardan foydalan"
        ),
    ),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# 2. Agent va Executor
agent_runnable = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent = AgentExecutor(agent=agent_runnable, tools=tools, verbose=True)

# 3. Xotira doyo'ri
_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
  if session_id not in _store:
    _store[session_id] = InMemoryChatMessageHistory()
  return _store[session_id]


# 4. RunnableWithMessageHistory (parametr nomlari to'g'rilandi)
agent_with_memory = RunnableWithMessageHistory(
    agent,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="output",
)


def ask(session_id: str, text: str) -> str:
  cfg = {"configurable": {"session_id": session_id}}
  result = agent_with_memory.invoke({"input": text}, config=cfg)
  return result.get("output", str(result))


if __name__ == "__main__":
  session_id = "sherale-session"
  print(ask(session_id, "Meni ismim Sherale"))
  print(ask(session_id, "O`zbekistondagi poytaxti qayer?"))
  print(ask(session_id, "5 kupaytirsa 10 nima qanday javob chiqadi"))
  print(ask(session_id, "Meni ismim nima?"))