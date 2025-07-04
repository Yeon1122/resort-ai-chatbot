# evaluation.py - RAGAS 평가 코드 (get_recycling_answer 활용)
import os
import sys
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

# ✅ rag_module.py 경로 추가 및 함수 import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "backend", "utils")))
from rag_module import get_recycling_answer

# ✅ 환경 변수 로드
load_dotenv()

# ✅ 질문 및 정답 데이터
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

# ✅ 평가 데이터셋 구축
dataset_dict = {"question": [], "answer": [], "contexts": [], "ground_truth": []}

for q, gt in zip(questions, ground_truth):
    # get_recycling_answer는 내부에서 retriever와 LLM을 사용해 응답 생성
    answer = get_recycling_answer(image_item=None, question=q)

    # retriever 문맥도 별도로 수집
    from rag_module import vector_db
    retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    docs = retriever.invoke(q)
    context_list = [doc.page_content for doc in docs]

    dataset_dict["question"].append(q)
    dataset_dict["answer"].append(answer)
    dataset_dict["contexts"].append(context_list)
    dataset_dict["ground_truth"].append(gt)

# ✅ 평가 실행
dataset = Dataset.from_dict(dataset_dict)

result = evaluate(dataset, [
    context_precision,
    context_recall,
    answer_relevancy,
    faithfulness,
    answer_similarity
])

print("\n✅ RAGAS 평가 결과")
print(result)
