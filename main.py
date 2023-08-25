from fastapi import FastAPI
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

from database import SessionLocal
from models import *


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/schedulers")
async def scheduler_list():
    db = SessionLocal()
    _scheduler_list = db.query(Scheduler).order_by(Scheduler.id).all()
    db.close()
    return _scheduler_list

# @app.post("/schedulers")
# async def create_scheduler():
#