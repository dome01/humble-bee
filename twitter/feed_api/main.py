from fastapi import FastAPI, HTTPException, APIRouter
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@app.get("/feed")
def get_feed(username: str):
    res_follows = supabase.table("follows").select("followed_username").eq("follower_username", username).execute()
    if not res_follows.data:
        return []
    followed_usernames = [f["followed_username"] for f in res_follows.data]
    res_posts = supabase.table("posts").select("*").in_("username", followed_usernames).order("created_at", desc=True).execute()
    if res_posts.data is None:
        raise HTTPException(status_code=404, detail="No posts found")
    return res_posts.data