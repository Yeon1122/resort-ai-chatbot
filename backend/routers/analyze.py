from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from schemas.analyze import AnalyzeResponse
from utils.yolo_infer import predict_topk_items_with_confidence
from utils.rag_module import get_recycling_answer

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(None),
    question: str = Form(None)
):
    # ✅ 빈 문자열인 file을 None으로 처리
    if isinstance(file, str) and file.strip() == "":
        file = None

    if not file and not question:
        raise HTTPException(status_code=400, detail="이미지 또는 질문 중 하나는 필요합니다.")

    try:
        candidates = []
        best_item = None
        best_conf = 0.0

        # 1. 이미지 → YOLO 품목 후보 추론
        if file:
            candidates = await predict_topk_items_with_confidence(file, top_k=3)

        # 2. 질문 + 이미지 → 가장 높은 confidence의 품목 사용
        if file and question:
            best_item = candidates[0]["item"]
            best_conf = candidates[0]["conf"]

        # 3. 질문만 입력 → 질문을 품목으로 간주
        elif question:
            best_item = question
            best_conf = 0.0

        # 4. 이미지만 입력 → 가장 높은 확률의 품목 사용
        elif file:
            best_item = candidates[0]["item"]
            best_conf = candidates[0]["conf"]

        # ✅ 5. 분리배출 방법 안내 생성
        answer = get_recycling_answer(f"{best_item}은(는) 어떻게 버려?")

        return AnalyzeResponse(item=best_item, confidence=best_conf, answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
