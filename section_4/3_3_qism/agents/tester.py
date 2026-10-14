from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool("execute_python")
def execute_python_code(code:str) -> str:
    """Run Python code and return the result"""
    print("[Tool] execute_python_code is called!")
    try:
        local_vars={}
        exec(code,{}, local_vars)
        return "Code executed successfully!"
    except Exception as e:
        return f"Error: {e}"

llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=1)

agent = create_react_agent(llm,[execute_python_code])

def tester_node(state):
    messages = [
        {"role":"user","content":f"Test this python code and response with PASS or FAIL: \n{state['code']}"}]

    response = agent.invoke({"messages": messages})

    final_message = response["message"][-1].content

    if "PASS" in final_message.upper():
        result = "PASS"
    elif "FAIL" in final_message.upper():
        result = "FAIL"
    else :
        result = "ERROR"
    return {"result":result , "details":final_message}
