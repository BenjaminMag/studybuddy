#NiceGUI example code
"""
from fastapi import FastAPI
from database import engine, Base
from routers import auth
from services import groups, filesharing, chat, tasks

# Creation of the database tables

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Study-Buddy API", version="1.0.0")

# Include the routers

app.include_router(auth.router)
app.include_router(groups.router)
app.include_router(filesharing.router)
app.include_router(chat.router)
app.include_router(tasks.router)
@app.get("/")
def root():
    return {"message": "Welcome to the Study-Buddy API!"}
    """