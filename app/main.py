from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import frame_router, record_router, user_session_router

APP_TITLE = "Internship FastAPI Sample"
APP_VERSION = "1.0"
APP_DESCRIPTION = "This is a internship FastAPI sample."

app = FastAPI(title=APP_TITLE,
              version=APP_VERSION,
              description=APP_DESCRIPTION)

origins = [
    "https://localhost",
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(record_router)
app.include_router(user_session_router)
app.include_router(frame_router)
