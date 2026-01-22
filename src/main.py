from fastapi import FastAPI, HTTPException
from typing import List

from src.api.models import Document
from src.services.mq_publisher import publish_documents

app = FastAPI(title="Search Service", version="1.0.0")


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/v1/documents", status_code=202)
def submit_documents(documents: List[Document]):
    if not documents:
        raise HTTPException(status_code=400, detail="Document list cannot be empty")

    publish_documents([doc.dict() for doc in documents])
    return {"message": "Documents accepted for indexing"}
