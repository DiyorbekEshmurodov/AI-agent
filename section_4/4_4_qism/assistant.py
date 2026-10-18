from typing import TypedDict , List,Dict,Literal
from langgraph.graph import StateGraph, START , END
import ollama
from audio import detect_wake_work,transcriber,speak

class VoiceAssistantState(TypedDict):
    message: List[str,str]
    user_input: str
    response: str

class VoiceAssistantAgent:
    def __init__(self):
        self.graph = self._setup_langgraph()

    def _setup_langgraph(self):
        graph_builder = StateGraph(VoiceAssistantState)

        graph_builder.add_node("wait_wake_word",self._wait_wake_word)
        graph_builder.add_node("listen_input",self._listen_input)
        graph_builder.add_node("process_conversation",self._process_conversation)
        graph_builder.add_node("generate_response",self._generate_response)
        graph_builder.add_node("speak_response",self._speak_response)

        graph_builder.add_edge(START, "wait_wake_word")
        graph_builder.add_edge("wait_wake_word", "listen_input")
        graph_builder.add_edge("listen_input", "process_conversation")
        graph_builder.add_edge("process_conversation", "generate_response")
        graph_builder.add_edge("generate_response", "speak_response")

        graph_builder.add_edge("speak_response", "wait_wake_word")

        return graph_builder.compile()

    def run(self):
        state = VoiceAssistantState(
            message=[],
            user_input="",
            response_text=""
        )
        self.graph.invoke(state)

    def _wait_wake_word(self,state:VoiceAssistantState) -> VoiceAssistantState:
        detect_wake_work()
        return state

    def _listen_input(self,state:VoiceAssistantState) -> VoiceAssistantState:
        user_text = transcriber()
        state["user_input"] = user_text
        state['messages'].append({'role':'user','content':user_text})
        return state

    def _process_conversation(self,state:VoiceAssistantState) -> VoiceAssistantState:
        state['messages'].append({'role': 'user', 'content': "Thinking..."})
        return state

    def _generate_response(self, state: VoiceAssistantState) -> VoiceAssistantState:
        prompt = state["user_input"]
        response = ollama.chat(model="gemma3:1b",
                               messages=[{"role": "user",
                                          "content": "Generate short answers without any symbols, only characters: " + prompt}])
        reply = response["message"]["content"]
        state["response_text"] = reply
        state["messages"].append(
            {"role": "assistant", "content": reply})
        print(f"Assistant: {reply}")
        return state

    def _speak_response(self, state: VoiceAssistantState) -> VoiceAssistantState:
        speak(state["response_text"])
        return state