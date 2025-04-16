from fastapi import FastAPI, Request, UploadFile, File, Form
from pydantic import BaseModel
from app.langchain_pipeline import ask_question, get_history_by_user, init_pipeline
from app.knowledge_loader import list_documents, delete_document
from app.config import DOCS_PATH, MEMORY_CACHE
import shutil
import os

app = FastAPI()

class Question(BaseModel):
    user_id: str
    question: str

@app.post("/ask")
async def ask(q: Question):
    result = ask_question(q.question, user_id=q.user_id)
    return {
        "user_id": q.user_id,
        "question": q.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }

@app.get("/history/{user_id}")
async def get_history(user_id: str):
    history = get_history_by_user(user_id)
    return {"user_id": user_id, "history": history}

@app.post("/refresh")
async def refresh_index():
    init_pipeline(force_refresh=True)
    return {"status": "Vector index refreshed successfully."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported."}
    os.makedirs(DOCS_PATH, exist_ok=True)
    file_path = os.path.join(DOCS_PATH, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "File uploaded successfully.", "filename": file.filename}

@app.get("/docss")
async def get_docs():
    return {"documents": list_documents(DOCS_PATH)}

@app.post("/docss/delete")
async def delete_doc(filename: str = Form(...)):
    success = delete_document(DOCS_PATH, filename)
    return {"deleted": success, "filename": filename}

@app.get("/status")
async def get_status():
    from time import time
    if os.path.exists(DOCS_PATH):
        doc_count = len(list_documents(DOCS_PATH))
    else:
        doc_count = 0
    ts = 0.0
    if os.path.exists("data/vectorstore/last_update.txt"):
        with open("data/vectorstore/last_update.txt") as f:
            ts = float(f.read().strip())
    return {"doc_count": doc_count, "last_update": ts, "timestamp_now": time()}

@app.post("/user/reset")
async def reset_user(user_id: str = Form(...)):
    MEMORY_CACHE[user_id] = []
    return {"cleared": True, "user_id": user_id}
