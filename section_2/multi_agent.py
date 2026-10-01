import os
import json
import urllib.parse
import urllib.request
from typing import Dict
from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=1,timeout=30,max_retries=1)

def _fx_convert_impl(amount:float, base:str, target:str) -> dict:
    base_up , target_up = base.upper(), target.upper()
    url = f"https://open.er-api.com/v6/latest/{base_up}"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read())
    rate = data['rates'][target_up]
    result = rate * amount
    return {
        "amount": amount,
        "base":base,
        "target":target_up,
        "rate":rate,
        "result":result,
        "date":data['time_last_update_utc']
    }
@tool
def fx_convert(amount: float, base: str, target: str) -> str:
    """Valyutalarni o'zaro ayirboshlash va kursni hisoblash funksiyasi (masalan: USD, EUR, UZS)."""
    try:
        res = _fx_convert_impl(amount,base,target)
        return (
            f"{res['amount']} {res['base']} = {res['result']} {res['target']}"
            f"(rate {res['rate']} , date {res['date']})"
        )
    except Exception as e:
        return f"Conversion failed {e}"

currency_tool = [fx_convert]
currency_prompt = ChatPromptTemplate.from_messages([
    ("system","You are the Currency Agent.ONLY handle currency conversion using fx_convert tool."),
    ("human","{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

currency_agent_runnable = create_tool_calling_agent(
    llm=llm, tools=currency_tool,prompt=currency_prompt)
currency_agent = AgentExecutor(
    agent=currency_agent_runnable, tools=currency_tool,max_iterations=3)

# ================================================================================================= #
wiki_api = WikipediaAPIWrapper(lang="en",top_k_results=2,doc_content_chars_max=1200,headers={"User-Agent": "MyTravelAgent/1.0 (contact@example.com)"})
@tool
def safe_wikipedia_tool(query: str) -> str:
  """Search Wikipedia for destination facts, culture, and travel information."""
  try:
    wiki_run = WikipediaQueryRun(api_wrapper=wiki_api)
    return wiki_run.run(query)
  except Exception as e:
    return f"Wikipedia bilan ulanishda xatolik yuz berdi: {e}"

travel_tool=[safe_wikipedia_tool]
travel_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are the travel Guide Agent. Fetch concise travel-relevant"
            " facts and tips using safe_wikipedia_tool, Focus on highlights,"
            " neighborhoods, transport, must-see spots."
        ),
    ),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

travel_agent_runnable = create_tool_calling_agent(
    llm=llm, tools=travel_tool,prompt=travel_prompt)
travel_agent = AgentExecutor(
    agent=travel_agent_runnable, tools=travel_tool,max_iterations=3)
# ================================================================================================= #

@tool
def currency_agent_tool(task: str)->str:
    """Delegate currency-related tasks(amount/base/target) in the Currency agent"""
    out = currency_agent.invoke({'input':task})
    return out.get('output',str(out))

@tool
def travel_agent_tool(task:str)->str:
    """Delegate destination information queries in the Travel Guide agent"""
    out = travel_agent.invoke({'input':task})
    return out.get('output',str(out))

coord_tools = [currency_agent_tool , travel_agent_tool]

coord_prompt = ChatPromptTemplate.from_messages([
    ("system","You are the Coordinator Agent. Understand the user`s goal, than call th right role agent"
     "User currency_agent_tool for any currency conversions"
     "User travel_tool_agent for destination info"
     "If both are needed, call both and product a single, well-structured answer."
     "Remember user preferences from the conversation"),
    MessagesPlaceholder('chat_history'),
    ("human","{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

coord_agent_runnable = create_tool_calling_agent(
    llm=llm, tools=coord_tools,prompt=coord_prompt)
coord_agent = AgentExecutor(
    agent=coord_agent_runnable, tools=coord_tools)


# 3. Xotira doyo'ri
_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
  if session_id not in _store:
    _store[session_id] = InMemoryChatMessageHistory()
  return _store[session_id]


# 4. RunnableWithMessageHistory (parametr nomlari to'g'rilandi)
agent_with_memory = RunnableWithMessageHistory(
    coord_agent,
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
  print(ask(session_id, "Parijdagi qaysi muzeydi tavsiya qilasiz?"))
  print(ask(session_id, "Sayohat uchun 500 USD bor bu pul miqdori EUR qancha buladi?"))
