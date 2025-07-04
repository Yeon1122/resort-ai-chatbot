# Re:sort - 분리배출 도우미 챗봇
SSAFY 13기 AI 코스 대전 2팀

Re:sort는 사용자가 버리려는 쓰레기를 사진으로 찍거나 간단한 질문을 입력하면, 
이미지를 분석하여 품목을 분류하거나, 자연어 질문을 이해해 환경부 가이드라인에 따라 정확한 분리배출 방법을 안내해주는 AI 챗봇 서비스입니다.
YOLO를 활용한 이미지 분류 + RAG 기반 문서 검색 + LLM 응답 생성을 통해 사용자에게 정확하고 빠른 분리배출 안내를 제공합니다.
### 배포 링크
- 서비스 배포 주소 : https://dev.d1bnkyl237hpbt.amplifyapp.com

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
RESORT-AI-CHATBOT/
├── src/                          # 서비스 구현 코드 전체
│   ├── backend/                  # FastAPI 기반 백엔드 서버
│   │   ├── models/               # 데이터베이스 모델 정의
│   │   ├── routers/              # API 라우터 정의
│   │   ├── schemas/              # Pydantic 스키마 정의
│   │   ├── utils/                # YOLO, RAG 모듈 구현
│   │   │   ├── rag_module.py
│   │   │   └── yolo_infer.py
│   │   └── main.py               # FastAPI 서버 진입점
│   │
│   ├── data/                     # 데이터 파일 및 전처리 결과
│   │   ├── input/                # 환경부 분리배출 가이드라인 원본 PDF
│   │   └── output/               # 전처리된 HTML, 평가결과 저장
│   │
│   └── frontend/                 # React + Vite 프론트엔드 프로젝트
│       ├── public/
│       ├── src/                  # React 컴포넌트, 페이지
│       ├── index.html
│       ├── tailwind.config.js
│       ├── vite.config.js
│       └── ...
│
├── test/                         # 평가/테스트용 스크립트
│   ├── test_images/              # 이미지 기반 평가용 테스트 이미지
│   │   ├── glass_bottle.png
│   │   ├── milk_pack.png
│   │   └── aluminum_can.png
│   ├── evaluation_image.py       # 이미지 기반 RAG 평가 코드
│   ├── evaluation_question.py    # 질문 기반 RAG 평가 코드
│   ├── .env.sample               # 테스트용 환경변수
│   └── eval_requirements.txt     # 평가에 필요한 패키지 목록
│
├── requirements.txt              # 설치 패키지
└── README.md

```

- `backend/` : FastAPI 기반 API 서버, YOLO로 이미지 인식 + LLM으로 분리배출 안내   
- `data/` : 분리배출 PDF 문서 전처리 및 RAG 파이프라인 구현   
- `frontend/` : 사용자가 이미지를 업로드하고 응답을 받을 수 있는 웹 인터페이스   
- `docs/` : 최종 산출물 보관

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
- **문서검색**: LangChain, Pinecone
- **LLM**: Upstage Chat API
- **기타**: AWS 배포
---

## 참고
- [환경부 분리배출 가이드라인 PDF](https://www.me.go.kr/home/web/public_info/read.do?pagerOffset=0&maxPageItems=10&maxIndexPages=10&searchKey=&searchValue=&menuId=10344&orgCd=&condition.code=A&condition.typeCode=A&typeCode=A&publicInfoId=17468&menuId=10344)
- [AI Hub 폐기물 이미지 데이터셋](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=120)
