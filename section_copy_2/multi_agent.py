import json
import urllib.parse
import urllib,requests
from typing import Dict
from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor , create_tool_calling_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=1,timeout=30,max_retries=1)

def _fx_convert_impl(amount:float, base:str, target:str) -> dict:
    base_up , target_up = base.upper(),target.upper()
    url = f"https://open.er-api.com/v6/latest/{base_up}"
    with urllib.request.urlopen(url , timeout=10) as response:
        data = json.loads(response.read())
    rate = data['rate'][target_up]
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
    """Valyutalarni o`zara ayirboshlash va kursni hisoblash funksiyasi (masalan : USD,EUR,UZS)."""
    try :
        res = _fx_convert_impl(amount, base, target)
        return (
            f"{res['amount']} {res['base']} = {res['result']} {res['target']}"
            f"(rate {res['rate']} , date {res['date']})"
        )
    except Exception as e:
        return f"Conversion failed {e}"

currenc_tool = [fx_convert]
currency_prompt = ChatPromptTemplate.from_messages([
    ("system","You are the Currency Agent .Only handle currency conversion using fx_convert tool."),
    ("human","{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])



