import os
from dotenv import load_dotenv
from groq import Groq

# 1. .env faylidan kalitni yuklaymiz
load_dotenv()

# 2. Groq mijozini yaratamiz
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# 3. So'rov yuboramiz (Llama 3 modeli orqali)
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "user", "content": "Salom! AI agent nima?"}
    ]
)

# 4. Javobni chop etamiz
print(response.choices[0].message.content)