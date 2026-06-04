import json
import os

def _load_contacts():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "2000_moz.json")
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)

def _load_phonebook():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "phonebook.json")
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)

_PHONE_INDEX = {c["phone_number"]: c for c in _load_contacts()}
_PHONE_INDEX.update({c["phone_number"]: c for c in _load_phonebook()})

def execute_momo_transfer(phone_number: str, amount: int = None) -> str:
    """
    CHỈ GỌI CÔNG CỤ NÀY SAU KHI ĐÃ KIỂM TRA AN TOÀN (safety_check).
    Sử dụng công cụ này để tạo ra Deep-link mở màn hình chuyển tiền MoMo.
    Người dùng sẽ không bị trừ tiền ngay, mà chỉ mở màn hình điền sẵn thông tin.

    Args:
        phone_number: Số điện thoại người nhận.
        amount: Số tiền muốn chuyển (nếu người dùng chưa cung cấp thì bỏ trống).
    """
    deeplink = f"momo://transfer?phone={phone_number}"
    if amount:
        deeplink += f"&amount={amount}"

    contact = _PHONE_INDEX.get(phone_number)
    recipient_name = contact["full_name"] if contact else phone_number

    return json.dumps({
        "status": "success",
        "action": "trigger_deeplink",
        "deeplink": deeplink,
        "recipient_name": recipient_name,
        "message_to_user": f"Đang mở màn hình chuyển tiền MoMo tới {recipient_name}..."
    }, ensure_ascii=False)
