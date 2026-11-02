
import os
import uvicorn
import requests
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

app = FastAPI()

LLM_URL = os.environ["LLM_URL"]

class Query(BaseModel):
    prompt: str
    model : str

@app.post("/ask")
async def ask(query: Query):
    try:
        response = requests.post(f"{LLM_URL}/api/generate", 
        json={"model":query.model, 
              "prompt":query.prompt,
              "stream":False
              }
        )
        response.raise_for_status()
        return {"answer": response.json()["response"]}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)


