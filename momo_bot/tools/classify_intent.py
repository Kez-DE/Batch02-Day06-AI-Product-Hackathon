import json

def classify_intent(query: str) -> str:
    """
    (Optional Tool) Giúp phân loại rõ ràng ý định của người dùng nếu hệ thống có nhiều tính năng (Hỏi đáp, Chuyển tiền, Nạp tiền...).
    Hiện tại ứng dụng chỉ tập trung vào luồng chuyển tiền.
    """
    if "chuyển" in query.lower() or "tiền" in query.lower() or "pay" in query.lower():
        return json.dumps({"intent": "TRANSFER_MONEY", "confidence": 0.95})
    return json.dumps({"intent": "UNKNOWN", "confidence": 0.5})
