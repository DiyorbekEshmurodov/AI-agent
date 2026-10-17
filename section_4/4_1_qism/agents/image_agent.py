from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


async def setup_image_agent():
    client = MultiServerMCPClient({
        "image": {
            "command": "python",
            "args": ["mcp_servers/image_server.py"],
            "transport": "stdio",
        }
    })
    tools = await client.get_tools()

    # llm = ChatGroq(
    #     model="deepseek-r1-distill-llama-70b",
    #     temperature=0.4)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.4)
    return create_react_agent(llm, tools)


async def image_node(state):
    image_agent = await setup_image_agent()
    response = await image_agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": f"Generate a thumbnail image for this LinkedIn post: \n {state['post_text']}"
        }]
    })
    return {"image_path": "outputs/image.png"}
