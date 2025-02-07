from supabase import Client, create_client
from fastapi import FastAPI
from dotenv import load_dotenv
import os

app = FastAPI()

# Initialize Supabase client
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
