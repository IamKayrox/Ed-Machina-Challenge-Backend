from fastapi import FastAPI

from .routers import leads, subjects, inscriptions

app = FastAPI()

app.include_router(leads.router)
app.include_router(subjects.router)
app.include_router(inscriptions.router)