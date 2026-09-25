import asyncio
import sys

# Windows tizimidagi Event Loop muammosini hal etish
if sys.platform == 'win32':
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from typing import Dict
import chainlit as cl
from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_groq import ChatGroq
import nest_asyncio

load_dotenv()
nest_asyncio.apply()

_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
  if session_id not in _store:
    _store[session_id] = InMemoryChatMessageHistory()
  return _store[session_id]


@cl.on_chat_start
async def start():
  llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0)
  search_tools = DuckDuckGoSearchRun()

  @tool
  def multiply(a: int, b: int):
    """Ikkita sonni bir-biriga ko'paytiruvchi funksiya."""
    return a * b

  tools = [search_tools, multiply]

  prompt = ChatPromptTemplate.from_messages([
      (
          "system",
          (
              "Sen yordamchi agentsan. ReAct sifatida fikr yurit va kerak bo'lsa"
              " foydali vositalardan foydalan."
          ),
      ),
      MessagesPlaceholder("chat_history"),
      ("human", "{input}"),
      MessagesPlaceholder("agent_scratchpad"),
  ])

  agent_runnable = create_tool_calling_agent(
      llm=llm, tools=tools, prompt=prompt
  )
  agent = AgentExecutor(agent=agent_runnable, tools=tools, verbose=True)

  agent_with_memory = RunnableWithMessageHistory(
      agent,
      get_session_history,
      input_messages_key="input",
      history_messages_key="chat_history",
      output_messages_key="output",
  )

  cl.user_session.set("agent", agent_with_memory)


@cl.on_message
async def main(message: cl.Message):
  agent = cl.user_session.get("agent")
  session_id = cl.user_session.get("id")

  cfg = {"configurable": {"session_id": session_id}}

  res = await cl.make_async(agent.invoke)({"input": message.content}, config=cfg)

  response_text = (
      res.get("output", str(res)) if isinstance(res, dict) else str(res)
  )
  await cl.Message(content=response_text).send()