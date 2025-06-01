from fastapi import FastAPI, HTTPException, APIRouter
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

router = APIRouter(prefix="/api/v1")

@router.post("/posts")
def create_post(username: str, content: str):
    res = supabase.table("posts").insert({
        "username": username,
        "content": content
    }).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Error creating post")
    return res.data[0]

app.include_router(router)