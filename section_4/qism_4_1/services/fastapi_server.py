from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel
from section_4.qism_4_1.graph_builder import build_graph

graph = build_graph()
app = FastAPI()

class RequestBody(BaseModel):
    topic: str

@app.post("/generate_post")
async def generate_post(body:RequestBody):
    state = {"topic":body.topic}
    result = await graph.ainvoke(state)
    return {
        "post_text": result.get("post_text"),
        "image_path": result.get("image_path")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("section_4.qism_4_1.services.fastapi_server:app", host="127.0.0.1", port=8000, reload=True)
