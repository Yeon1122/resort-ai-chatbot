# Postgre_chunkEmbedding.py

import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain_upstage import UpstageEmbeddings
from langchain.docstore.document import Document
import matplotlib.pyplot as plt

# .env 로드
load_dotenv()
upstage_key = os.getenv("UPSTAGE_API_KEY")
connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

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


# # ✅ 3. 시각화 함수
# def plot_split_lengths(splits):
#     split_lengths = [len(split.page_content) for split in splits]
#     plt.bar(range(len(split_lengths)), split_lengths)
#     plt.title("RecursiveCharacterTextSplitter")
#     plt.xlabel("Split Index")
#     plt.ylabel("Split Content Length")
#     plt.xticks(range(len(split_lengths)), [])
#     plt.show()


# # 시각화 실행 예시
# plot_split_lengths(splits)


# ✅ 4. 벡터스토어 저장
vectorstore = PGVector.from_documents(
    documents=splits,
    embedding=UpstageEmbeddings(model="embedding-query"),
    connection_string=connection_string,
    collection_name="chatbot_vectors",
    pre_delete_collection=True  # (선택) 새로 덮어쓰기
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

