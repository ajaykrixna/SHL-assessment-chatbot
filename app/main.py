from fastapi import FastAPI
from pydantic import BaseModel

from app.chat import chat

app = FastAPI()


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    return chat(request.query)