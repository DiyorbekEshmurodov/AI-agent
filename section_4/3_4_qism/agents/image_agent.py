from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def setup_image_agent():
    client = MultiServerMCPClient({
        "image":{
            "command":"python",
            "args":["mcp_server/image.server.py"],
            "transport":"stdio"
        }
    })

    tools = await client.get_tools()
    llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.4)
    return create_react_agent(llm,tools)

async def image_node(state):
    image_agent = await setup_image_agent()
    response = await image_agent.ainvoke({
        "message":[{
            "role":"user",
            "content":f"Generate a thumbnail image for this LinkedIn post: \n {state['post_text']}"
        }]
    })

    return {"image_path": response["message"[-1].content]}