from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from uuid import uuid4
from dotenv import load_dotenv
import os
from supabase import create_client, Client


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
def home():
    return "Hello from ID-Gen!"

@app.post("/ids")
def create_id():
    new_id = str(uuid4())
    supabase.table("ids").insert({"id": new_id}).execute()
    return {"id": new_id}