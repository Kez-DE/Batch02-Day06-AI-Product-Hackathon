from .clarify import clarify_contact
from .safety_check import safety_check
from .momo_next_action import execute_momo_transfer
from .classify_intent import classify_intent

# Danh sách các tool function
AGENT_TOOLS = [
    clarify_contact,
    safety_check,
    execute_momo_transfer,
    classify_intent
]

# Định nghĩa JSON Schemas cho OpenAI Function Calling
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "clarify_contact",
            "description": "Công cụ này được sử dụng khi người dùng nhắc đến một tên mơ hồ (ví dụ: 'chuyển cho mẹ', 'chuyển anh Long') mà chưa có số điện thoại cụ thể. Nó sẽ tìm kiếm trong danh bạ và trả về các lựa chọn để bạn hỏi lại người dùng.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name_hint": {"type": "string", "description": "Tên hoặc từ khóa người dùng nhắc tới (ví dụ: 'mẹ', 'long')."}
                },
                "required": ["name_hint"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "safety_check",
            "description": "Sử dụng công cụ này ĐỂ KIỂM TRA TÍNH AN TOÀN TRƯỚC KHI tạo lệnh chuyển tiền, khi bạn đã có được số điện thoại chính xác. Nó kiểm tra xem số điện thoại có lừa đảo không, hoặc số tiền có quá lớn không.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_number": {"type": "string", "description": "Số điện thoại người nhận (vd: '0912345678')."},
                    "amount": {"type": "integer", "description": "Số tiền muốn chuyển (nếu có)."}
                },
                "required": ["phone_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_momo_transfer",
            "description": "CHỈ GỌI CÔNG CỤ NÀY SAU KHI ĐÃ KIỂM TRA AN TOÀN (safety_check). Sử dụng công cụ này để tạo ra Deep-link mở màn hình chuyển tiền MoMo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_number": {"type": "string", "description": "Số điện thoại người nhận."},
                    "amount": {"type": "integer", "description": "Số tiền muốn chuyển."}
                },
                "required": ["phone_number"]
            }
        }
    }
]
