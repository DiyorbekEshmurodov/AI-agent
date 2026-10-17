from constants import (
    JOB_DESCRIPTION,
    MIN_YEARS,
    MUST_HAVE_SKILLS,
    NICE_TO_HAVE_SKILLS,
    THRESHOLD
)
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    from graph_builder import build_graph
    graph = build_graph()
    resume_path = input("Path to resume (PDF/TXT):").strip()

    initial_state ={
        "resume_path":resume_path,
        "job_description": JOB_DESCRIPTION,
        "min_years":MIN_YEARS,
        "must_have_skills":MUST_HAVE_SKILLS,
        "nice_to_have_skills": NICE_TO_HAVE_SKILLS,
        "threshold" : THRESHOLD,
    }
    final_state = graph.invoke(initial_state)

    print("===============Screening result==============")
    print("Decision: ",final_state.get("decision"))
    print("Score: ",final_state.get("score"))
    print("Reasons:")
    for r in final_state.get("reasons",[]):
        print(" - ",r)
    print("Improvments: ")
    for i in final_state.get("improvments",[]):
        print(" - ",r)


if __name__ == "__main__" :
    main()