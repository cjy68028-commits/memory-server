from fastapi import FastAPI
from typing import Dict, List

app = FastAPI()

memory_store: Dict[str, List[str]] = {}

@app.get("/")
def home():
    return {"status": "memory server running"}

@app.get("/memory")
def get_memory(user_id: str):
    return memory_store.get(user_id, [])

@app.post("/memory/add")
def add_memory(user_id: str, content: str):
    memory_store.setdefault(user_id, []).append(content)
    return {"ok": True}

@app.post("/memory/update")
def update_memory(user_id: str, index: int, content: str):
    if user_id in memory_store and index < len(memory_store[user_id]):
        memory_store[user_id][index] = content
    return {"ok": True}
