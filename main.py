from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

from job import job_router

# 라우터 등록
app.include_router(job_router.router)