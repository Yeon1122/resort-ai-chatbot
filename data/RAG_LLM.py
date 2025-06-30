# utils/rag_module.py

import os
import sys
import warnings
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 경고 숨기기
warnings.filterwarnings("ignore")

# .env 파일 로드
load_dotenv()
upstage_key = os.getenv("UPSTAGE_API_KEY")

# ✅ 벡터스토어 로드 (telemetry 경고 무시)
with open(os.devnull, 'w') as devnull:
    old_stderr = sys.stderr
    sys.stderr = devnull
    try:
        vectorstore = Chroma(
            embedding_function=UpstageEmbeddings(model="embedding-query"),
            persist_directory='./output/chroma_db'
        )
    finally:
        sys.stderr = old_stderr

# ✅ LLM 및 Chain 구성
llm = ChatUpstage()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            당신은 질문의 주어에 집중해서 주어진 CONTEXT(문맥) 안에서만 답변하는 정직하고 정확한 답변 비서입니다.
            아래 CONTEXT 내용에 기반하여 질문에 답변하세요.
            만약 CONTEXT에 충분한 정보가 없다면 모르는 부분은 솔직하게 "주어진 문맥만으로는 알 수 없습니다."라고 대답하세요.
            추가적인 상상이나 문맥에 없는 내용을 만들어내지 마세요.

            가능하면 답변은 간결하고 이해하기 쉽게 작성하세요. 내용이 중복되지 않도록 답변하세요.
            ---
            CONTEXT:
            {context}
            """
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm | StrOutputParser()

# ✅ 외부에서 사용 가능한 RAG 기반 응답 함수
def get_recycling_answer(query: str) -> str:
    retriever = vectorstore.as_retriever(
        search_type='mmr',
        search_kwargs={"k": 3}
    )

    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            result_docs = retriever.invoke(query)
        finally:
            sys.stderr = old_stderr

    context = "\n\n".join([doc.page_content for doc in result_docs])

    response = chain.invoke({
        "context": context,
        "input": query
    })

    return response
