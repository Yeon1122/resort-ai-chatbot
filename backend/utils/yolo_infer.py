from ultralytics import YOLO
import os
import numpy as np
import cv2
from fastapi import UploadFile

# ✅ 모델 전역 변수 선언
model = None

# ✅ 영어 → 한글 라벨 매핑
label_mapping = {
    "paper": "종이",
    "can": "캔",
    "glass": "유리",
    "plastic": "플라스틱",
    "vinyl": "비닐",
    "styrofoam": "스티로폼",
    "battery": "건전지",
    "trash": "쓰레기",
    "multi_mat": "복합 재질",
}


# ✅ 비동기 YOLO 추론 함수
async def predict_topk_items_with_confidence(file: UploadFile, top_k: int = 3):
    global model

    # ❗최초 1회만 모델 로드
    if model is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "best.pt")
        model = YOLO(model_path)

    contents = await file.read()

    # ✅ 이미지 바이트 → numpy 배열
    file_bytes = np.asarray(bytearray(contents), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return [{"item": "이미지 디코딩 실패", "conf": 0.0}]

    # ✅ YOLO 추론
    results = model.predict(
        source=img,
        imgsz=640,
        conf=0.01,
        save=False
    )

    # ✅ 클래스 이름 및 예측 결과 추출
    names = model.names
    predictions = results[0].boxes

    items = []
    for box in predictions:
        cls_id = int(box.cls[0].item())
        conf = float(box.conf[0].item())
        label_en = names[cls_id]
        label_ko = label_mapping.get(label_en, label_en)
        items.append({
            "item": label_ko,
            "conf": round(conf, 3)
        })

    return sorted(items, key=lambda x: x["conf"], reverse=True)[:top_k]
