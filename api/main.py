import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from supabase import Client, create_client

# Initialize Supabase client
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()


# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Pydantic models
class UserRegister(BaseModel):
    username: str  # Treat username as email
    password: str


class UserLogin(BaseModel):
    username: str  # Treat username as email
    password: str


class UserProfile(BaseModel):
    email: str | None = None

# Register a new user


@app.post("/register")
async def register(user: UserRegister):
    try:
        # Register user with Supabase (treat username as email)
        response = supabase.auth.sign_up({"email": user.username, "password": user.password})

        # Insert username into profiles table
        user_id = response.user.id
        supabase.table("profiles").insert({
            "id": user_id,
            "username": user.username,
            "email": None  # Email can be added later
        }).execute()

        return {"message": "User registered successfully", "data": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Login and get access token


@app.post("/login")
async def login(user: UserLogin):
    try:
        # Authenticate user with Supabase (treat username as email)
        response = supabase.auth.sign_in_with_password({"email": user.username, "password": user.password})
        return {"access_token": response.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Add or update email in profile


@app.post("/profile/email")
async def update_email(profile: UserProfile, token: str = Depends(oauth2_scheme)):
    try:
        # Get user ID from token
        user = supabase.auth.get_user(token)
        user_id = user.user.id

        # Update email in profiles table
        supabase.table("profiles").update({"email": profile.email}).eq("id", user_id).execute()
        return {"message": "Email updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get user profile


@app.get("/profile")
async def get_profile(token: str = Depends(oauth2_scheme)):
    try:
        # Get user ID from token
        user = supabase.auth.get_user(token)
        user_id = user.user.id

        # Fetch profile from profiles table
        profile = supabase.table("profiles").select("*").eq("id", user_id).execute()
        return {"profile": profile.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def read_root():
    return {"Hello": "World"}
