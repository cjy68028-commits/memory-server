from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI()

memory_store: Dict[str, List[str]] = {}


class SearchRequest(BaseModel):
    user_id: str
    query: str


class SaveRequest(BaseModel):
    user_id: str
    content: str


class UpdateRequest(BaseModel):
    user_id: str
    index: int
    content: str


@app.get("/")
def home():
    return {"status": "memory server running"}


@app.get("/memory")
def get_memory(user_id: str):
    return memory_store.get(user_id, [])


@app.post("/memory/add")
def add_memory(req: SaveRequest):
    memory_store.setdefault(req.user_id, []).append(req.content)
    return {"ok": True}


@app.post("/memory/update")
def update_memory(req: UpdateRequest):
    if req.user_id in memory_store and 0 <= req.index < len(memory_store[req.user_id]):
        memory_store[req.user_id][req.index] = req.content
        return {"ok": True}
    return {"ok": False, "error": "memory not found"}


@app.post("/search")
def search_memory(req: SearchRequest):
    memories = memory_store.get(req.user_id, [])

    results = []
    for item in memories:
        if req.query in item or item in req.query:
            results.append({"content": item})

    if not results:
        results = [{"content": item} for item in memories[-8:]]

    return {"results": results}


@app.post("/save")
def save_memory(req: SaveRequest):
    memory_store.setdefault(req.user_id, []).append(req.content)
    return {"ok": True}
