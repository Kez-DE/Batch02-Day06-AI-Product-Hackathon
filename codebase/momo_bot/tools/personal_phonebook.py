import json
import os
import unicodedata


def _load_phonebook():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "phonebook.json")
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)


_PHONEBOOK = _load_phonebook()


def _normalize(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text.lower().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def lookup_personal_contact(name_hint: str) -> str:
    """
    Tra cứu danh bạ cá nhân của chủ tài khoản từ data/phonebook.json.

    Args:
        name_hint: Tên, biệt danh hoặc quan hệ người dùng nhắc tới (ví dụ: "mẹ", "vợ", "con trai").
    """
    key = _normalize(name_hint)
    results = []

    for contact in _PHONEBOOK:
        full_name = contact.get("full_name", "")
        alias = contact.get("Alias", "")
        searchable_text = _normalize(f"{full_name} {alias}")

        if key in searchable_text or any(key in part for part in searchable_text.split()):
            results.append({
                "name": full_name,
                "phone": contact.get("phone_number"),
                "alias": alias,
                "source": "personal_phonebook"
            })

    if not results:
        return json.dumps({
            "status": "not_found",
            "message": f"Không tìm thấy '{name_hint}' trong danh bạ cá nhân. Có thể thử `clarify_contact` hoặc hỏi người dùng số điện thoại cụ thể."
        }, ensure_ascii=False)

    action = "use_contact" if len(results) == 1 else "ask_user_to_choose"
    return json.dumps({
        "status": "success",
        "action": action,
        "options": results,
        "message": "Nếu chỉ có một kết quả phù hợp, dùng số này để gọi safety_check. Nếu có nhiều kết quả, hỏi người dùng chọn đúng người nhận."
    }, ensure_ascii=False)
