from typing import Dict
import os

from langchain_community.document_loaders import PyPDFLoader,TextLoader

def loader_node(state:Dict) -> Dict:
    """
    Input:
        state['resume_path'] -> path to PDF or TXT
    Output:
        {'resume_txt': "..."}
    """
    path = state['resume_path']
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        docs = PyPDFLoader(path).load()
        text = "\n\n".join([d.page_content for d in docs])
    else:
        docs = TextLoader(path,encoding='utf-8').load()
        text = "\n\n".join([d.page_content for d in docs])

    return {"resume_txt": text}