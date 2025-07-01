# pine_chunkEmbedding.py

import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_upstage import UpstageEmbeddings
from langchain.docstore.document import Document
import matplotlib.pyplot as plt

# .env 로드
load_dotenv()
upstage_key = os.getenv("UPSTAGE_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

#********************************************
print("pinecone 연결 시작")
# pinecone 연결
pc = Pinecone(api_key=pinecone_api_key)
# 인덱스 이름 지정
index_name = "resort-chatbot"

if index_name not in pc.list_indexes().names():
    print(f"인덱스 {index_name}가 존재하지 않습니다. 생성합니다.")
    pc.create_index(
        name=index_name,
        dimension=4096,
        metric="cosine",
        spec=ServerlessSpec(
            cloud = "aws",
            region = "us-east-1"
        )
    )
else:
    print(f"인덱스 {index_name}가 존재합니다.")

print("pinecone 연결 완료")
#********************************************
# 1. HTML 파싱해서 페이지별로 Document 리스트 만들기
html_path = "./output/parsed_output.html"

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

pages = []
current_page = []
for elem in soup.children:
    if elem.name is not None:
        current_page.append(str(elem))
        if elem.name == "footer":
            pages.append("\n".join(current_page))
            current_page = []

if current_page:
    pages.append("\n".join(current_page))

page_docs = [Document(page_content=page) for page in pages]
print(f"총 {len(page_docs)}개의 페이지로 나누어짐.")


# ✅ 2. 청크화
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=300
)
splits = text_splitter.split_documents(page_docs)

print("Splits:", len(splits))


# ✅ 3. 시각화 함수
def plot_split_lengths(splits):
    split_lengths = [len(split.page_content) for split in splits]
    plt.bar(range(len(split_lengths)), split_lengths)
    plt.title("RecursiveCharacterTextSplitter")
    plt.xlabel("Split Index")
    plt.ylabel("Split Content Length")
    plt.xticks(range(len(split_lengths)), [])
    plt.show()


# 시각화 실행 예시
plot_split_lengths(splits)


# ✅ 4. 벡터스토어 저장
# 임베딩 함수
print("임베딩 함수 생성 시작")
embeddings = UpstageEmbeddings(model="embedding-query")

print("vectorstore 생성 시작")
# Pinecone VectorStore 생성
vectorstore = PineconeVectorStore.from_documents(
    documents=splits,
    embedding=embeddings,
    index_name=index_name
)

"""
실행시 터미널에 나오는 이 문구 무시 가능.
Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given
Failed to send telemetry event ClientCreateCollectionEvent: capture() takes 1 positional argument but 3 were given
Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given
Failed to send telemetry event ClientCreateCollectionEvent: capture() takes 1 positional argument but 3 were given
"""

print("벡터스토어 저장 완료")
# Chroma는 자동으로 영구 저장되므로 persist() 호출이 필요하지 않음

