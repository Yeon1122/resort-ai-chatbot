from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from schemas.analyze import AnalyzeResponse
from utils.yolo_infer import predict_topk_items_with_confidence
from utils.rag_module import get_recycling_answer
from typing import List

router = APIRouter()

known_items = sorted([
    # 플라스틱류
    "페트병", "플라스틱용기", "플라스틱병", "플라스틱뚜껑", "플라스틱컵", "플라스틱",
    
    # 금속/캔류
    "알루미늄캔", "철캔", "부탄가스", "스프레이캔", "캔",

    # 종이류
    "종이", "신문지", "책자", "박스", "종이팩", "우유팩", "종이컵",

    # 유리병
    "소주병", "맥주병", "음료수병", "유리병",

    # 비닐/필름류
    "비닐봉지", "과자봉지", "라면봉지", "비닐포장재", "비닐",

    # 스티로폼
    "스티로폼", "완충재",

    # 의류
    "의류", "옷",

    # 폐건전지/형광등
    "폐건전지", "전지", "형광등", "전구",

    # 아이스팩 등
    "아이스팩", "보냉팩",

    # 음식물 쓰레기 (혼동 방지용)
    "음식물", "음식물쓰레기",

    # 일반쓰레기
    "기저귀", "휴지", "면봉", "칫솔", "일반쓰레기"
], key=len, reverse=True)


def extract_known_items_by_question_order(question: str) -> List[str]:
    matches = []
    temp_question = question  # 변경용 사본

    for item in known_items:
        idx = temp_question.find(item)
        if idx != -1:
            matches.append((idx, item))
            temp_question = temp_question.replace(item, " " * len(item))  # 중복 방지

    # 질문 등장 순서대로 정렬
    matches.sort(key=lambda x: x[0])
    return [item for _, item in matches]


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(None),
    question: str = Form(None)
):
    if isinstance(file, str) and file.strip() == "":
        file = None

    if not file and not question:
        raise HTTPException(status_code=400, detail="이미지 또는 질문 중 하나는 필요합니다.")

    try:
        candidates = []
        image_item = None
        image_conf = 0.0
        # question_item = None
        best_item = ""
        answer = ""
        question_items = []
        # 1. 이미지가 있을 경우 → YOLO 예측
        if file:
            candidates = await predict_topk_items_with_confidence(file, top_k=3)
            image_item = candidates[0]["item"]
            image_conf = candidates[0]["conf"]
        # 2. 질문이 있을 경우 → 질문을 품목으로 간주
        if question:
            question_items = extract_known_items_by_question_order(question.strip())

        # 3. 이미지 + 질문 둘 다 있는 경우
        if image_item and question_items:
            if image_item not in question_items:
                image_answer = get_recycling_answer(f"{image_item}은(는) 어떻게 버려?")
                question_answers = [
                    f"{item}: {get_recycling_answer(f'{item}은(는) 어떻게 버려?')}"
                    for item in question_items
                ]
                answer = (
                    f"### 🖼️ 이미지 분석 결과\n\n"
                    f"- 인식된 품목: **{image_item}**\n"
                    f"- 안내: {image_answer}\n\n"
                    f"---\n\n"
                    f"### 🗣️ 질문에서 인식된 품목\n\n"
                    + "".join([f"- {qa}\n" for qa in question_answers])
                )
                best_item = f"{image_item} / {' / '.join(question_items)}"
            else:
                answer = get_recycling_answer(f"{image_item}은(는) 어떻게 버려?")
                best_item = image_item
                image_conf = candidates[0]["conf"]

        # 4. 질문만 있는 경우
        elif question_items:
            question_answers = [
                f"{item}: {get_recycling_answer(f'{item}은(는) 어떻게 버려?')}"
                for item in question_items
            ]
            answer = "\n".join(question_answers)
            best_item = " / ".join(question_items)
            image_conf = 0.0

        # 5. 이미지만 있는 경우
        elif image_item:
            answer = get_recycling_answer(f"{image_item}은(는) 어떻게 버려?")
            best_item = image_item
            image_conf = candidates[0]["conf"]


        if not best_item:
            best_item = "알 수 없음"
        if not answer:
            answer = "분리배출 정보를 찾지 못했습니다."


        return AnalyzeResponse(item=best_item, confidence=image_conf, answer=answer)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
