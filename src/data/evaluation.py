# evaluation.py
# GroundTruth안 넣은 버전.

import os
from dotenv import load_dotenv

from langchain_pinecone import Pinecone as PineconeVectorStore
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from pinecone import Pinecone
from datasets import Dataset
import numpy as np
import matplotlib.pyplot as plt

# ✅ ragas import
from ragas.evaluation import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    answer_relevancy,
    faithfulness,
    answer_similarity
)

# ✅ .env 로드
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
upstage_key = os.getenv("UPSTAGE_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

# ✅ Pinecone 연결
pc = Pinecone(api_key=pinecone_api_key)
index_name = "resort-chatbot"
index = pc.Index(index_name)

# ✅ VectorStore 핸들러
embeddings = UpstageEmbeddings(model="embedding-query")
pinecone_vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="text"
)

# ✅ Retriever 생성
pinecone_retriever = pinecone_vectorstore.as_retriever(
    search_type='mmr',
    search_kwargs={"k": 3}
)

# ✅ LLM
llm = ChatUpstage()

pinecone_data = {
    "question": [],
    "answer": [],
    "contexts": [],
    "ground_truth": []
}

# ✅ 평가 질문 예시
questions = [
    "신문지는 어떻게 배출해야 하나요?",
    "종이컵 배출할 때 주의할 점은?",
    "종이팩과 종이류는 왜 구분해서 버려야 하나요?",
    "금속캔에 담배꽁초가 들어있으면 어떻게 해야 하나요?",
    "유리병 뚜껑은 같이 배출해도 되나요?",
    "빈 소주병은 어떻게 처리해야 하나요?",
    "페트병 라벨은 어떻게 처리하나요?",
    "스티로폼 접시는 어떻게 배출해야 하나요?",
    "플라스틱 용기 안 내용물은 어떻게 해야 하나요?",
    "플라스틱 병뚜껑은 어떻게 버려요?",
    "아이스팩은 어떻게 버리나요?",
    "에어캡은 어떤 분류로 배출하나요?",
    "깨진 유리는 어떻게 버려야 하나요?",
    "폐건전지는 어떻게 버려야 하나요?",
    "폐형광등은 어떻게 배출하나요?",
    "폐의약품은 어디로 버려야 하나요?",
    "음식물 쓰레기로 버리면 안 되는 것은?",
    "종량제 봉투로 버려야 하는 종이는?",
    "불연성 폐기물은 어떻게 버려야 하나요?",
    "가전제품은 어떻게 배출해야 하나요?"
]

ground_truth = [
    "신문지는 물기에 젖지 않도록 펴서 차곡차곡 쌓고 끈으로 묶어 배출한다.",
    "종이컵은 내용물을 비우고 깨끗이 헹군 뒤 말려서 배출한다.",
    "종이팩과 종이류는 서로 다른 재활용 공정을 거치기 때문에 구분하여 배출한다.",
    "금속캔은 내용물을 비우고 이물질을 제거한 뒤 담배꽁초는 넣지 않고 배출한다.",
    "유리병 뚜껑은 철이나 알루미늄이므로 함께 배출한다.",
    "소주병, 맥주병 등 빈용기보증금 대상 병은 소매점에 반납해 보증금을 환급받는다.",
    "페트병 라벨과 뚜껑은 분리해서 별도로 배출한다.",
    "스티로폼 접시는 내용물을 비우고 깨끗이 헹군 뒤 비닐랩은 제거하고 배출한다.",
    "플라스틱 용기 안 내용물은 깨끗이 비우고 헹궈서 배출한다.",
    "플라스틱 병뚜껑은 본체에서 분리해 플라스틱류로 배출한다.",
    "아이스팩은 겉 비닐과 내용물을 분리해 겉 비닐은 깨끗하게 배출한다.",
    "에어캡(뽁뽁이)은 비닐류로 배출한다.",
    "깨진 유리는 신문지로 싸서 종량제 봉투에 버린다.",
    "폐건전지는 전용수거함에 배출한다.",
    "폐형광등은 깨지지 않게 전용수거함에 배출한다.",
    "폐의약품은 약국이나 보건소에 비치된 전용수거함으로 배출한다.",
    "복어 내장, 생선뼈, 조개껍질 등은 음식물쓰레기로 배출하면 안 된다.",
    "감열지 영수증, 코팅된 종이는 종량제 봉투로 배출한다.",
    "불연성 폐기물(백열전구, 깨진 도자기 등)은 전용봉투에 담아 배출한다.",
    "대형 가전제품은 무상 방문 수거 서비스를 신청해 배출한다."
]

# ✅ 문맥 생성 함수
def fill_data(data, question, retriever, gt):
    result_docs = retriever.invoke(question)
    contexts = [doc.page_content for doc in result_docs]

    prompt = f"질문: {question}\n\n문맥: {contexts}\n\n\
                당신은 질문의 주어에 집중해서 주어진 CONTEXT(문맥) 안에서만 답변하는 정직하고 정확한 답변 비서입니다.\
                아래 CONTEXT 내용에 기반하여 질문에 답변하세요.\
                만약 CONTEXT에 충분한 정보가 없다면 모르는 부분은 솔직하게 \"주어진 문맥만으로는 알 수 없습니다.\"라고 대답하세요.\
                추가적인 상상이나 문맥에 없는 내용을 만들어내지 마세요.\n\n\
                가능하면 답변은 간결하고 이해하기 쉽게 작성하세요. 내용이 중복되지 않도록 답변하세요."
    answer_obj = llm.invoke(prompt)
    
    answer = answer_obj.content

    data["question"].append(question)
    data["answer"].append(answer)
    data["contexts"].append(contexts)
    data["ground_truth"].append(gt)

# ✅ 루프 돌려서 데이터셋 만들기
for q, gt in zip(questions, ground_truth):
    fill_data(pinecone_data, q, pinecone_retriever, gt)

pinecone_dataset = Dataset.from_dict(pinecone_data)

# ✅ ragas 평가 로직
metrics = [
    context_precision,
    context_recall,
    answer_relevancy,
    faithfulness,
    answer_similarity
]

result = evaluate(pinecone_dataset, metrics)

print("\n✅ RAGAS 평가 결과")
print(result)
# ✅ 간이 Precision & Recall & Accuracy 계산
# (실제로는 ragas 쓰면 더 정밀함)

# 여기서는 Retriever가 가져온 문맥 개수로 대략 계산 예시
# k=3 기준 → 가져온 문맥이 많을수록 Recall↑
# Precision = Accuracy로 가정



#----------------------------------------------------------------------------------------------------------
# 그래프로 제작해서 보려고 했는데 밑에 로직 이상해서 무시하셔도 됩니다.

# context_precision = [len(ctx) / 3 for ctx in pinecone_data["contexts"]]
# context_recall = [min(len(ctx) / 3, 1.0) for ctx in pinecone_data["contexts"]]

# precision = np.nanmean(context_precision)
# recall = np.nanmean(context_recall)
# accuracy = precision  # Retriever만 평가 시 보통 동일 취급

# print(f"Pinecone Precision: {precision:.4f}")
# print(f"Pinecone Recall: {recall:.4f}")
# print(f"Pinecone Accuracy: {accuracy:.4f}")

# # ✅ 그래프로 시각화 (Precision + Recall + Accuracy)
# fig, ax = plt.subplots()

# metrics = ['Precision', 'Recall', 'Accuracy']
# scores = [precision, recall, accuracy]

# bars = ax.bar(metrics, scores, color=['steelblue', 'orange', 'green'])

# for rect in bars:
#     height = rect.get_height()
#     ax.annotate(f'{height:.2f}',
#                 xy=(rect.get_x() + rect.get_width() / 2, height),
#                 xytext=(0, 3),
#                 textcoords="offset points",
#                 ha='center', va='bottom')

# ax.set_ylim(0, 1)
# ax.set_title("Pinecone Vector DB: Precision, Recall, Accuracy")
# plt.tight_layout()
# plt.show()
