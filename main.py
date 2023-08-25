from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database import get_db
import models_schema
from models import *

from typing import List


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/schedulers", response_model=List[models_schema.Scheduler])
async def scheduler_list(db: Session = Depends(get_db)):
    _scheduler_list = db.query(Scheduler).order_by(Scheduler.id).all()
    return _scheduler_list

# @app.post("/schedulers")
# async def create_scheduler():
