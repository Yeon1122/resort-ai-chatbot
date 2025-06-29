## RAG_LLM 실행 방법
- Chroma_db의 인덱스 자체가 100MB를 넘어서 git 자체에 올리지 못하기 때문에, 각자 pull 받은 후 다음과 같은 순서로 실행 부탁드립니다.

```
1.가상환경 제작 후 pip install -r requirements.txt
2. .env파일에 upstrage에서 받은 api키 추가
3. 가상 환경 킨 후 chunkEmbedding.py => RAG_LLM.py 순으로 키면 됩니다.
4. 안 돌아갈 시 가장 먼저 pdf2html.py 실행 부탁드립니다.
```
