import os
from contextlib import asynccontextmanager
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://127.0.0.1:8003/generate_post"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = os.getenv("PUBLIC_URL") + "/webhook"
    requests.get(f"{BASE_URL}/setWebhook?url={webhook_url}")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def telegram_webhook(request: Request):
    print('Data received')
    data = await request.json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        topic = data["message"]["text"]

        response = requests.post(API_URL, json={"topic": topic}).json()

        post_text = response.get("post_text", "Failed to generate post")
        image_path = response.get("image_path")

        requests.post(f"{BASE_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": post_text
        })

        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as img:
                requests.post(f"{BASE_URL}/sendPhoto",
                              data={"chat_id": chat_id},
                              files={"photo": img})

    return {"ok": True}
