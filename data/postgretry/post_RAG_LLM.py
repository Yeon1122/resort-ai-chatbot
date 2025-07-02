# post_RAG_LLM.py

import os
import sys
import warnings
from dotenv import load_dotenv
from langchain_community.vectorstores import PGVector
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pprint

# 경고 메시지 숨기기
warnings.filterwarnings("ignore")


# .env 로드
load_dotenv()
upstage_key = os.getenv("UPSTAGE_API_KEY")
connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

# stderr를 /dev/null로 리다이렉트
with open(os.devnull, 'w') as devnull:
    old_stderr = sys.stderr
    sys.stderr = devnull
    try:
        # 여기에 벡터스토어 로드 코드
        vectorstore = PGVector(
            embedding_function=UpstageEmbeddings(model="embedding-query"),
            connection_string=connection_string,
            collection_name="chatbot_vectors"
        )
    finally:
        sys.stderr = old_stderr

# # ✅ 저장된 벡터스토어 로드
# vectorstore = Chroma(
#     embedding_function=UpstageEmbeddings(model="embedding-query"),
#     persist_directory='./output/chroma_db'
# )


#=======================================================================================================
# # ✅ Retriever 생성 [기반 문서 확인 및 top-k 조절]
# query = "에어캡은 어떻게 버려?"
# retriever = vectorstore.as_retriever(
#     search_type='mmr',
#     search_kwargs={"k": 3}
# )

# result_docs = retriever.invoke(query)

# print(f"검색된 문서 개수: {len(result_docs)}")

# if len(result_docs) > 0:
#     pprint.pprint(result_docs[0].page_content[:1000])
#     print("--------------------------------")
#     if len(result_docs) > 1:
#         pprint.pprint(result_docs[1].page_content[:1000])
#         print("--------------------------------")
#     if len(result_docs) > 2:
#         pprint.pprint(result_docs[2].page_content[:1000])
#         print("--------------------------------")
# else:
#     print("검색 결과가 없습니다.")
#     exit()

#=======================================================================================================

# ✅ LLM Chain
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
            """,
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm | StrOutputParser()

# ✅ 질문 예시
query = input("질문을 입력하세요: ").encode("utf-8").decode("utf-8")

retriever = vectorstore.as_retriever(
    search_type='mmr',
    search_kwargs={"k": 3}
)

# stderr 리다이렉트로 telemetry 메시지 숨기기
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

print()
print()
print("--------------------------------")
print(f"질문: {query}")
print("--------------------------------")
print(f"챗봇 답변: {response}")

