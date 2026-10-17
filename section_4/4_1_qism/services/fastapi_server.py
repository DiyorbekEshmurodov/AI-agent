from fastapi import FastAPI
from pydantic import BaseModel
from graph_builder import build_graph


graph = build_graph()
app = FastAPI()


class RequestBody(BaseModel):
    topic: str


@app.post("/generate_post")
async def generate_post(body: RequestBody):
    state = {"topic": body.topic}
    result = await graph.ainvoke(state)
    return {
        "post_text": result.get("post_text"),
        "image_path": result.get("image_path")
    }
