from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from utils.yolo_infer import predict_topk_items_with_confidence
from utils.rag_module import get_recycling_answer

router = APIRouter()

# 전역 대화 이력 (최근 5개만 유지)
chat_history = []

def build_prompt():
    prompt = ""
    for turn in chat_history[-5:-1]:
        prompt += f"Q: {turn['human']}\nA: {turn['system']}\n"
    return prompt

@router.post("/test")
async def test_analyze(
    file: UploadFile = File(None),
    question: str = Form(None)
):
    if isinstance(file, str) and file.strip() == "":
        file = None

    if not file and not question:
        raise HTTPException(status_code=400, detail="이미지 또는 질문 중 하나는 필요합니다.")

    try:
        candidates = []
        best_item = None
        best_conf = 0.0
        human_text = ""

        # 1. 이미지 → YOLO 품목 후보 추론
        if file:
            candidates = await predict_topk_items_with_confidence(file, top_k=3)

        # 2. 질문 + 이미지
        if file and question:
            best_item = candidates[0]["item"]
            best_conf = candidates[0]["conf"]
            human_text = f"(이미지포함, 인식된 품목: {best_item}) {question}"
        # 3. 질문만
        elif question:
            best_item = ""
            best_conf = 0.0
            human_text = question
        # 4. 이미지만
        elif file:
            best_item = candidates[0]["item"]
            best_conf = candidates[0]["conf"]
            human_text = f"(이미지포함, 인식된 품목: {best_item})"

        # 프롬프트에 대화 이력 포함
        prompt = build_prompt() + f"Q: {human_text}\nA:"

        # 답변 생성
        answer = get_recycling_answer(prompt)

        # 이력에 추가
        chat_history.append({"human": human_text, "system": answer})
        if len(chat_history) > 5:
            chat_history.pop(0)

        # 전체 이력 반환
        return {
            "history": chat_history,
            "item": best_item,
            "confidence": best_conf,
            # "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))