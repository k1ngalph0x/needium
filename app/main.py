
import os
import uvicorn
import requests
from config.settings import settings
from schemas.schema import QueryRequest
from fastapi import FastAPI, HTTPException, UploadFile, File

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

@app.post("/api/doc")
async def upload_files(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_path": file_path
    }

@app.post("/api/ask")
async def ask(query: QueryRequest):
    try:
        response = requests.post(
            f"{settings.LLM_URL}/api/generate",
            json={
                "model": QueryRequest.model,
                "prompt": QueryRequest.prompt,
                "stream": False
            }
            )
        response.raise_for_status()
        return {"answer":response.json()["response"]}
    except requests.RequestException as exc:
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)


    

