import json
import os
import unicodedata

def _load_contacts():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "2000_moz.json")
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)

_CONTACTS = _load_contacts()

def _normalize(text: str) -> str:
    """Lowercase + strip diacritics so 'Ngoc' matches 'Ngọc'."""
    nfkd = unicodedata.normalize("NFKD", text.lower().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def clarify_contact(name_hint: str) -> str:
    """
    Công cụ này được sử dụng khi người dùng nhắc đến một tên mơ hồ (ví dụ: 'chuyển cho mẹ', 'chuyển anh Long') mà chưa có số điện thoại cụ thể.
    Nó sẽ tìm kiếm trong danh bạ và trả về các lựa chọn để bạn (AI) hỏi lại người dùng.

    Args:
        name_hint: Tên hoặc từ khóa người dùng nhắc tới (ví dụ: 'mẹ', 'long').
    """
    key = _normalize(name_hint)

    results = []
    for contact in _CONTACTS:
        name = _normalize(contact["full_name"])
        if key in name or any(key in part for part in name.split()):
            results.append({
                "name": contact["full_name"],
                "phone": contact["phone_number"],
                "province": contact["province"]
            })
        if len(results) >= 5:
            break

    if not results:
        return json.dumps({
            "status": "not_found",
            "message": f"Không tìm thấy ai tên '{name_hint}' trong danh bạ. Vui lòng hỏi người dùng số điện thoại cụ thể."
        }, ensure_ascii=False)

    return json.dumps({
        "status": "success",
        "action": "ask_user_to_choose",
        "options": results,
        "message": "Hãy hiển thị các lựa chọn này dưới dạng nút bấm (button) cho người dùng chọn."
    }, ensure_ascii=False)
