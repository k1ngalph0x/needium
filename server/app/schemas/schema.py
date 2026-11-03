from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

class QueryResponse(BaseModel):
    question: str
    context: list[str]
    answer: str