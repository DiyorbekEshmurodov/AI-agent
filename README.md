# AI-agent
Markdown
# AI Agent & LangChain Experiments

This repository demonstrates how to build and execute AI Agents using **LangChain (LCEL)**, **Groq API**, and **Hugging Face Transformers**. It serves as a practical guide for creating intelligent agents capable of handling complex prompts, translation tasks, and local NLP operations.

## 🚀 Features

- **Groq Integration:** Fast inference using `openai/gpt-oss-120b` and `llama-3.3-70b-versatile` models.
- **LangChain Expression Language (LCEL):** Modern pipeline construction using standard `prompt | llm` chains.
- **Local NLP with Transformers:** Text generation and processing using Hugging Face models (`distilbert/distilgpt2`).
- **Secure Environment:** Environment variable management using `python-dotenv`.

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain Core & LangChain Groq**
- **Hugging Face Transformers & PyTorch**
- **Groq API**

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/DiyorbekEshmurodov/AI-agent.git](https://github.com/DiyorbekEshmurodov/AI-agent.git)
   cd AI-agent
Create and activate a virtual environment:

Bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
Install dependencies:

Bash
pip install langchain-core langchain-groq transformers torch python-dotenv
Set up Environment Variables:
Create a .env file in the root directory and add your Groq API key:

Фрагмент кода
GROQ_API_KEY=your_actual_groq_api_key_here
💻 Usage Examples
1. LangChain Translation Chain
Run the translation script using modern LCEL syntax:

Bash
python agent_translate.py
2. Hugging Face Transformers Test
Run local text-generation models:

Bash
python test_transformers.py
📝 License
Distributed under the MIT License. See LICENSE for more information.
