from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, like
from .oauth2 import get_current_user
# from .config import settings
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()
CORS_ORIGINS = os.getenv('CORS_ORIGINS')

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router, dependencies=[ Depends(get_current_user) ])
app.include_router(like.router)
app.include_router(user.router)
app.include_router(auth.router)

