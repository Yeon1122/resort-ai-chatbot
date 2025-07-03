# Re:sort - 분리배출 도우미 챗봇
SSAFY 13기 AI 코스 대전 2팀

Re:sort는 이미지와 질문을 기반으로 사용자가 올바르게 분리배출할 수 있도록 도와주는 AI 챗봇 서비스입니다.
YOLO를 활용한 이미지 분류 + RAG 기반 문서 검색 + LLM 응답 생성을 통해 사용자에게 정확하고 빠른 분리배출 안내를 제공합니다.
### 배포 링크
- 서비스 배포 주소 : (추후 추가 예정입니다.)

---
   
## 작동 예시
### 이미지 첨부
-> "음료캔" 이미지 업로드
- YOLOv8 모델 : "캔"으로 예측
- RAG : 예측된 품목과 관련된 문서 검색
- LLM 답변 생성 : "캔은 재활용이 가능한 폐금속류로 분류되어 따로 분리해 버려야 합니다."

### 질문 입력
-> "플라스틱 병은 어떻게 버려야 해?"
- RAG : 질문 관련 문서 검색
- LLM 답변 생성 : "플라스틱: 플라스틱의 분리배출 방법은 재질과 오염도에 따라 달라집니다."

### 이미지  + 질문 입력
- YOLOv8 + RAG + LLM : 이미지 기반 + 질문 기반 동시 답변 출력  

---

## 폴더 구조
```
resort-ai-chatbot/
├── backend/                  # FastAPI 백엔드 서버
│   ├── models/               # YOLO 모델 파일
│   ├── routers/              # API 라우터
│   ├── schemas/              # 요청/응답 스키마
│   ├── utils/                # YOLO & RAG 기능 모듈
│   └── main.py               # 백엔드 진입점
│
├── data/                     # 문서 임베딩 및 RAG 파이프라인
│   ├── input/                # 분리배출 가이드라인 PDF
│   ├── output/               # HTML 변환 결과
│   ├── postgretry/           # PostgreSQL 관련 실험 코드
│   ├── chunkEmbedding.py     # 문서 임베딩
│   └── RAG_LLM.py            # RAG + LLM 실행
│
├── frontend/                 # React + Vite 프론트엔드
│   ├── public/               # 정적 리소스 (로고, 이미지)
│   ├── src/                  # 앱 소스코드
│   │   ├── pages/            # 주요 화면 페이지
│   │   └── components/       # 공통 컴포넌트
│   └── index.html            # 진입 HTML
│
├── docs/                     # 서비스 기획 및 보고서
│   ├── 1차/                  # 기획안
│   └── 2차/                  # 최종보고서
│
├── requirements.txt          # 전체 의존성
└── eval_requirements.txt     # 평가용 의존성
```

- `backend/` : FastAPI 기반 API 서버, YOLO로 이미지 인식 + LLM으로 분리배출 안내   
- `data/` : 분리배출 PDF 문서 전처리 및 RAG 파이프라인 구현   
- `frontend/` : 사용자가 이미지를 업로드하고 응답을 받을 수 있는 웹 인터페이스   
- `docs/` : 서비스 기획안과 최종 산출물 보관   

---

## 설치 및 실행 방법
### .env 파일에 환경 변수 설정
- `UPSTAGE_API_KEY`
- `PINECONE_API_KEY`
   
### 백엔드 실행
```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload
```
- 실행 주소 : http://localhost:8000/docs

   
### 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```
- 실행 주소 : http://localhost:5173

---

## Git 커밋 & 브랜치 규칙

### 브랜치 전략
- `main`: 배포용 (최신 안정 버전)
- `dev`: 전체 병합용 (기능 통합 브랜치)
- `frontend`: 프론트엔드 작업 전용
- `backend`: 백엔드 작업 전용
- `model`: YOLO 모델 학습/예측 작업 전용
- `data`: 텍스트 전처리, 임베딩, 벡터 저장 관련 작업 전용
- `docs`: 문서 작성 및 보고서 정리 전용

> 각 파트는 독립적으로 브랜치를 생성해 작업하고, `dev` 브랜치로 병합한 후 `main`으로 최종 배포합니다.

### 커밋 메시지 규칙
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `docs`: 문서 추가/수정
- `test`: 테스트 코드 추가
- `chore`: 기타 설정, 빌드 수정 등

**예시**:
```
feat: YOLO 예측 결과를 응답에 포함시키는 기능 추가  
fix: 이미지 업로드 시 발생하던 500 오류 수정
```

---

## 팀원
- PM: 이하연
- 데이터 처리: 조은경
- 모델 처리: 연제현
- 백엔드: 문빈
- 프론트엔드: 안덕현

---
## 기술 스택

- **프론트엔드**: React, Vite, Tailwind CSS
- **백엔드**: FastAPI, Uvicorn
- **모델**: YOLOv8 (ultralytics)
- **문서검색**: LangChain, Pinecone, FAISS
- **LLM**: Upstage Chat API
- **기타**: Docker, Fly.io 배포
---

## 참고
- [환경부 분리배출 가이드라인 PDF](https://www.me.go.kr/home/web/public_info/read.do?pagerOffset=0&maxPageItems=10&maxIndexPages=10&searchKey=&searchValue=&menuId=10344&orgCd=&condition.code=A&condition.typeCode=A&typeCode=A&publicInfoId=17468&menuId=10344)
- [AI Hub 폐기물 이미지 데이터셋](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=120)
