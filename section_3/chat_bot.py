from typing import Dict
from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=1)
emb= HuggingFaceEmbeddings(model='sentence-transformers/all-MiniLM-L6-v2')

persist_directory = './chroma.db'
if not os.path.exists(persist_directory):
    raise FileNotFoundError(
        f"Vector database not found at {persist_directory} . Run db_build.py first"
    )

vs = Chroma(embedding_function=emb,collection_name='customer_db',
                           persist_directory=persist_directory)

retriever = vs.as_retriever(search_kwargs={"k":3})

@tool
def db_search(text:str) -> str:
  """Mijoz savollariga javob berishi uchun knowledge base qidirish"""
  res = retriever.invoke(text)
  if not res:
      return "Hech narsa topilmadi"
  return "\n\n".join([f"{d.page_content} " for d in res])

tools = [db_search]

# 1. Prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "Siz mijozlarga xizmat kursatuvchi chatbotsiz.Faqat mavjud manbalardan foydalanib javob bering.Agar"
            "topilmasa tug`risini ayting"
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
  print(ask(session_id, "Sizning qaytarish siyosatingiz qanday?"))
  print(ask(session_id, "Sizning ish vaqtingiz qanday?"))
  print(ask(session_id, "Meni ismim nima?"))