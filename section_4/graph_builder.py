from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START , END
from agents.writer import writer_node
from agents.tester import  tester_node

class State(TypedDict):
    task:str
    code:str
    explanation:str
    result:str
    detail:str
    retries:int

MAX_RETRIES = 3
def route_decision(state:State) -> State:
    if state['result'] == 'PASS':
        return END
    elif state['retries'] >= MAX_RETRIES:
        return END
    state['retries'] += 1
    return 'writer'

def build_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("writer",writer_node)
    graph_builder.add_node("tester",tester_node)

    graph_builder.add_edge(START,'writer')
    graph_builder.add_edge('writer','tester')
    graph_builder.add_conditional_edges('tester',route_decision)
    return graph_builder.compile()