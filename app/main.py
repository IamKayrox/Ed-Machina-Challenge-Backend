import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import leads, subjects, inscriptions

app = FastAPI()

origins = [
    "http://localhost:5173"
]

originsString = os.environ.get("CORS_ORIGINS")
if originsString:
    origins = originsString.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(leads.router)
app.include_router(subjects.router)
app.include_router(inscriptions.router)