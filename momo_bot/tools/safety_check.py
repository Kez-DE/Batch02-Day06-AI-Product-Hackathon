import json
import os

def _load_contacts():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "2000_moz.json")
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)

_PHONE_INDEX = {c["phone_number"]: c for c in _load_contacts()}

BLACKLIST_PHONES = ["0123456789", "0999999999"]
MAX_AMOUNT_NO_OTP = 5000000  # 5 triệu

def safety_check(phone_number: str, amount: int = 0) -> str:
    """
    Sử dụng công cụ này ĐỂ KIỂM TRA TÍNH AN TOÀN TRƯỚC KHI tạo lệnh chuyển tiền, khi bạn đã có được số điện thoại chính xác.
    Nó kiểm tra xem số điện thoại có lừa đảo không, hoặc số tiền có quá lớn không.

    Args:
        phone_number: Số điện thoại người nhận (vd: '0912345678').
        amount: (Tùy chọn) Số tiền muốn chuyển.
    """
    # 1. Check định dạng SĐT cơ bản
    if len(phone_number) < 9 or len(phone_number) > 11:
        return json.dumps({
            "safe": False,
            "reason": "Số điện thoại không đúng định dạng.",
            "next_action": "abort_and_alert"
        }, ensure_ascii=False)

    # 2. Check Blacklist
    if phone_number in BLACKLIST_PHONES:
        return json.dumps({
            "safe": False,
            "reason": "CẢNH BÁO: Số điện thoại này nằm trong danh sách đen lừa đảo!",
            "next_action": "abort_and_alert"
        }, ensure_ascii=False)

    # 3. Tra cứu trong dữ liệu khách hàng thực
    contact = _PHONE_INDEX.get(phone_number)
    if contact:
        if contact["account_status"] != "active":
            return json.dumps({
                "safe": False,
                "reason": f"Tài khoản của {contact['full_name']} ({phone_number}) đang bị khóa hoặc không hoạt động.",
                "next_action": "abort_and_alert"
            }, ensure_ascii=False)

        if not contact["wallet_verified"]:
            return json.dumps({
                "safe": False,
                "reason": f"Ví MoMo của {contact['full_name']} ({phone_number}) chưa được xác minh.",
                "next_action": "abort_and_alert"
            }, ensure_ascii=False)

        if contact["risk_level"] == "high":
            return json.dumps({
                "safe": False,
                "reason": f"CẢNH BÁO: Tài khoản {phone_number} có mức rủi ro cao.",
                "next_action": "abort_and_alert"
            }, ensure_ascii=False)

    # 4. Check hạn mức
    if amount > MAX_AMOUNT_NO_OTP:
        return json.dumps({
            "safe": False,
            "reason": f"Số tiền {amount:,} VND vượt quá hạn mức chuyển nhanh. Yêu cầu xác thực OTP hoặc khuôn mặt.",
            "next_action": "abort_and_alert"
        }, ensure_ascii=False)

    recipient_name = contact["full_name"] if contact else "Không xác định"
    return json.dumps({
        "safe": True,
        "recipient_name": recipient_name,
        "message": f"Số điện thoại an toàn. Người nhận: {recipient_name}. Có thể tiến hành mở màn hình chuyển tiền.",
        "next_action": "call_execute_momo_transfer"
    }, ensure_ascii=False)
