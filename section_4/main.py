from dotenv import load_dotenv
load_dotenv()
def main():
    from graph_builder import build_graph
    graph = build_graph()
    task = input("Enter a Python task for the AI agent:")

    initial_state = {
        'task': task,
        'code':'',
        'explanation':'',
        'result':'',
        'details':'',
        'retries':0
    }
    final_state = None
    for event in graph.stream(initial_state,stream_mode='updates'):
        for node , update in event.items():
            final_state = {**(final_state or initial_state),**update}
    if final_state:
        print('==========FINAL RESULT================')
        print(f'Task: {final_state["task"]}')
        print(f'Code: \n')
        print(final_state['code'])
        print('Explanation: \n')
        print(f"Test result: {final_state['result']}")
        print(f"Details: {final_state['details']}")

if __name__ == '__main__':
    main()
