from fastapi import FastAPI, HTTPException, APIRouter
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@app.post("/users")
def create_user(username: str):
    res = supabase.table("users").insert({"username": username}).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Username already exists or insertion failed")
    return res.data[0]
    

@app.post("/follow")
def follow(follower_username: str, followed_username: str):
    if follower_username == followed_username:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    res = supabase.table("follows").insert({
        "follower_username": follower_username,
        "followed_username": followed_username
    }).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Already following or insertion failed")
    return {"message": "Followed successfully"}