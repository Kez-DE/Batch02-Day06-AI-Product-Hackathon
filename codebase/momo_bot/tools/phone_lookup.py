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


def _personal_contact_to_account(contact):
    return {
        "full_name": contact["full_name"],
        "phone_number": contact["phone_number"],
        "account_status": "active",
        "wallet_verified": True,
        "risk_level": "low",
        "source": "personal_phonebook",
        "alias": contact.get("Alias", "")
    }


_PHONE_INDEX = {c["phone_number"]: {**c, "source": "momo_customer_data"} for c in _load_contacts()}
_PHONE_INDEX.update({
    c["phone_number"]: _personal_contact_to_account(c)
    for c in _load_phonebook()
})


def lookup_phone_number(phone_number: str) -> str:
    """
    Tra cứu chủ sở hữu của một số điện thoại trong dữ liệu MoMo và danh bạ cá nhân.

    Args:
        phone_number: Số điện thoại cần tra cứu.
    """
    contact = _PHONE_INDEX.get(phone_number)
    if not contact:
        return json.dumps({
            "status": "not_found",
            "phone_number": phone_number,
            "message": f"Không tìm thấy thông tin người nhận cho số {phone_number}."
        }, ensure_ascii=False)

    return json.dumps({
        "status": "success",
        "phone_number": phone_number,
        "recipient_name": contact["full_name"],
        "account_status": contact.get("account_status", "active"),
        "wallet_verified": contact.get("wallet_verified", True),
        "risk_level": contact.get("risk_level", "low"),
        "source": contact.get("source", "unknown"),
        "alias": contact.get("alias", "")
    }, ensure_ascii=False)
