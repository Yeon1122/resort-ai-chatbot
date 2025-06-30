# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze  # ← 올바르게 라우터 import

app = FastAPI()

# CORS 설정 (필요시)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(analyze.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Re:Sort Backend!"}
