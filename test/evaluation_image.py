# evaluation_multimodal.py
import os
import sys
import asyncio
from dotenv import load_dotenv
from datasets import Dataset
from ragas.evaluation import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    answer_relevancy,
    faithfulness,
    answer_similarity
)

# ✅ 경로 설정 및 함수 import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "backend", "utils")))
from rag_module import get_recycling_answer, vector_db
from yolo_infer import predict_topk_from_bytes

load_dotenv()

retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 3})

# ✅ 평가용 이미지 & 질문 데이터
samples = [
    {
        "image_path": "./test_images/glass_bottle.png",
        "question": "이 병은 어떻게 버리나요?",
        "ground_truth": "깨진 유리는 신문지로 싸서 종량제 봉투에 버린다."
    },
    {
        "image_path": "./test_images/milk_pack.png",
        "question": "우유팩은 종이류로 버리면 되나요?",
        "ground_truth": "종이팩과 종이류는 서로 다른 재활용 공정을 거치기 때문에 구분하여 배출한다."
    },
    {
        "image_path": "./test_images/aluminum_can.png",
        "question": "이 캔 그냥 버려도 되나요?",
        "ground_truth": "금속캔은 내용물을 비우고 이물질을 제거한 뒤 담배꽁초는 넣지 않고 배출한다."
    }
]

metrics = [
    context_precision,
    context_recall,
    answer_relevancy,
    faithfulness,
    answer_similarity
]

results = {"question": [], "answer": [], "contexts": [], "ground_truth": [], "case": []}

def collect_contexts(query):
    docs = retriever.invoke(query)
    return [doc.page_content for doc in docs]

# ✅ 비동기 평가 루프
async def main():
    for case in ["question_only", "image_only", "multimodal"]:
        for sample in samples:
            image_item = None
            question = None

            # 🔍 YOLO 예측 (await 필수!)
            with open(sample["image_path"], "rb") as f:
                file_bytes = f.read()
                preds = predict_topk_from_bytes(file_bytes, top_k=1)
                image_item = preds[0]["item"]

            if case == "question_only":
                question = sample["question"]
                answer = get_recycling_answer(None, question)
                context = collect_contexts(question)

            elif case == "image_only":
                question = None
                answer = get_recycling_answer(image_item, None)
                context = collect_contexts(image_item)

            elif case == "multimodal":
                question = sample["question"]
                answer = get_recycling_answer(image_item, question)
                context = collect_contexts(f"{image_item} {question}")

            results["question"].append(question if question else f"(이미지: {image_item})")
            results["answer"].append(answer)
            results["contexts"].append(context)
            results["ground_truth"].append(sample["ground_truth"])
            results["case"].append(case)

    dataset = Dataset.from_dict(results)
    result = evaluate(dataset, metrics)

    print("\n✅ RAGAS 멀티모달 평가 결과")
    print(result)

# ✅ 실행
if __name__ == "__main__":
    asyncio.run(main())
