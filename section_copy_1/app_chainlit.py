"""
if sys.platform == 'win32':
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import chainlit as cl
import nest_asyncio
nest_asyncio.apply()
from typing import Dict
_store nima?
_store: Dict[str, InMemoryChatMessageHistory] = {}
@cl.author_rename qanday ish bajarayapti

  cfg = {"configurable": {"session_id": session_id}}

  res = await cl.make_async(agent.invoke)({"input": message.content}, config=cfg)

  response_text = (
      res.get("output", str(res)) if isinstance(res, dict) else str(res)
  )
  await cl.Message(content=response_text).send()
await cl.Message(
  content="Salom! Meni ismim Diyorbek, men sizning shaxsiy AI agentingizman. Sizga qanday yordam bera olaman?"
).send()
"""
import asyncio
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from typing import Dict
import chainlit as cl
from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor,create_tool_calling_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_groq import ChatGroq
import nest_asyncio

load_dotenv()
nest_asyncio.apply()

_store : Dict[str,InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]