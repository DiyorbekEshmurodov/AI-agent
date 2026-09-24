# import os
# from dotenv import load_dotenv
from openai import OpenAI

# 1. Avval .env faylini yuklaymiz
load_dotenv()

# 2. Keyin client yaratamiz
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 3. Chat completion so'rovini yuboramiz
response = client.chat.completions.create(
    model='gpt-5',  # yoki 'gpt-3.5-turbo' / 'gpt-4'
    messages=[
        {"role": "user", "content": "Salom AI agent nima ?"}
    ]
)

# 4. Javobni chop etamiz
print(response.choices[0].message.content)