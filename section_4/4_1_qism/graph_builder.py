from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

from agents.post_agent import post_node
from agents.image_agent import image_node


class State(TypedDict):
    topic: str
    post_text: str
    image_path: str


def build_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("post", post_node)
    graph_builder.add_node("image", image_node)

    graph_builder.add_edge(START, "post")
    graph_builder.add_edge("post", "image")
    graph_builder.add_edge("image", END)

    return graph_builder.compile()
