# backend/utils/rag_module.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_upstage import ChatUpstage
from dotenv import load_dotenv
import os

load_dotenv()

# Chroma DB 경로 설정
CHROMA_DB_DIR = "./output/chroma_db"

# 임베딩 모델 로드
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 벡터스토어 로드
vector_db = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embedding_model
)

# LLM 체인 구성
llm = ChatUpstage()

prompt = ChatPromptTemplate.from_messages([
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
])

rag_chain = prompt | llm | StrOutputParser()

# 🔍 핵심 함수
def get_recycling_answer(question: str) -> str:
    retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    return rag_chain.invoke({
        "context": context,
        "input": question
    })
