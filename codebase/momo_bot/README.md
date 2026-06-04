# Momo Bot - AI Product Lab Day 06 Prototype

Đây là dự án prototype (Agent) mô phỏng tính năng "Chuyển tiền thông minh" bằng văn bản, ứng dụng mô hình ReAct Agent và Function Calling.

## Cài đặt

1. Tạo môi trường ảo (khuyến nghị):
```bash
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
```

2. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

3. Cấu hình API Key:
- Copy file `.env.example` thành `.env`
- Điền ít nhất một key vào file `.env`: `OPENROUTER_API_KEY`, `OPENAI_API_KEY` hoặc `GEMINI_API_KEY`.

## Khởi chạy

Chạy script CLI để tương tác với Moni:
```bash
python chat.py
```

Chạy giao diện web Streamlit:
```bash
python -m streamlit run web.py
```
