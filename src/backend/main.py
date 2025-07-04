# main.py ###
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze  # ← 올바르게 라우터 import

app = FastAPI()
##
# 배포된 프론트 주소 (예: Vercel 주소)
allowed_origins = [
    "https://dev.d1bnkyl237hpbt.amplifyapp.com",  # 프로덕션용
]

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(analyze.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Re:Sort Backend!"}
