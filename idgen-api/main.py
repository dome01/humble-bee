from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from uuid import uuid4

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
def home():
    return "Hello from ID-Gen!"

@app.post("/ids")
def create_id():
    new_id = str(uuid4())
    return {"id": new_id}