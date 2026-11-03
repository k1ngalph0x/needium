from pydantic import BaseModel


class QueryRequest(BaseModel):
    prompt: str
    top_k: int = 3
    model: str = "llama3.2:latest"

class QueryResponse(BaseModel):
    question: str
    context: list[str]
    answer: str