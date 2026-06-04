import os
from dotenv import load_dotenv

def load_env():
    """Loads environment variables from .env file."""
    load_dotenv(override=True)

    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    openai_key     = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_key     = os.getenv("GEMINI_API_KEY", "").strip()

    if not openrouter_key and not openai_key and not gemini_key:
        print("\n⚠️ CẢNH BÁO: Không tìm thấy API Key nào.")
        print("Vui lòng cung cấp OPENROUTER_API_KEY, OPENAI_API_KEY, hoặc GEMINI_API_KEY trong file .env.\n")
        return False

    if openrouter_key:
        print("✅ Tìm thấy OPENROUTER_API_KEY")
    if openai_key:
        print("✅ Tìm thấy OPENAI_API_KEY")
    if gemini_key:
        print("✅ Tìm thấy GEMINI_API_KEY")

    return True
