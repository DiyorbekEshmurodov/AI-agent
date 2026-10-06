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

    }