# Python 3.10 slim 이미지를 사용
FROM python:3.10-slim

# libGL.so.1 설치를 위한 필수 패키지 추가
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 전체 backend 소스 복사
COPY . .

# Uvicorn으로 FastAPI 앱 실행 (포트 8080)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
