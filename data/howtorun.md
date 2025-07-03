## RAG_LLM 실행 방법
- Chroma_db의 인덱스 자체가 100MB를 넘어서 git 자체에 올리지 못하기 때문에, 각자 pull 받은 후 다음과 같은 순서로 실행 부탁드립니다.

```
1.가상환경 제작 후 pip install -r requirements.txt
2. .env파일에 upstrage에서 받은 UPSTAGE_API_KEY키 추가
3. .env파일에 mm단톡방에 올린 PINECONE_API_KEY키 추가 (or pinecone가서 직접 계정 생성하고 api key 받아보셔도 됩니다다)
3. 가상 환경 킨 후 pine_RAG_LLM.py 키면 됩니다.
4. 안 돌아갈 시 가장 먼저 pdf2html.py => pine_chunEmbedding.py => pine_Rag_LLM.py 순으로 실행 부탁드립니다.
```


## evaluation.py 평가 해보는 방법
- RAG_LLM.py 실행하는 라이브러리 버전들과 애매하게 버전이 호환이 안되어서 eval_requirements.txt 를 가상환경에 설치하셔서 측정하셔야 합니다.
- .env 에 넣어야할 것: UPSTAGE_API_KEY, PINECONE_API_KEY, OPENAI_API_KEY (pinecone과 openai 관련 키는 mm 톡방 확인할 것)


## 만약 postgres와 pgvector를 사용한다면 
- UPSTAGE_API_KEY, POSTGRES_CONNECTION_STRING 환경변수 지정해줄 것.