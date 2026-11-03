import ollama
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

loader = TextLoader("car_sample.txt")
raw_documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300, #500
    chunk_overlap = 50
)

documents = text_splitter.split_documents(raw_documents)

db = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

query = "Whats the price of SSC TUATARA"

relevant_docs = db.similarity_search(query, k=3)
context = relevant_docs

system_prompt = (
    "You are an assistant. Answer the user's question using ONLY the context provided below."
    f"Context: \n{context}"
)

response = ollama.chat(
    model="llama3.2:latest",
    messages=[
        {
            "role":"system", "content":"system_prompt"
        },
        {
            "role": "user", "content": query
        }
    ]
)

print(response)