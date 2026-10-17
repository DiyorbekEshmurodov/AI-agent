import asyncio
from dotenv import load_dotenv

load_dotenv()


async def main():
    from graph_builder import build_graph
    graph = build_graph()

    topic = input("Enter a topic for LinkedIn post: ")
    initial_state = {
        "topic": topic,
        "post_text": f"LinkedIn post about {topic}",
        "image_path": "",
    }

    final_state = await graph.ainvoke(initial_state)
    print(final_state['post_text'])
    print(final_state['image_path'])

if __name__ == "__main__":
    asyncio.run(main())
