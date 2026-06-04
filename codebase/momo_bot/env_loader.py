import os
from dotenv import load_dotenv

def load_env():
    """Loads environment variables from .env file."""
    load_dotenv()
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not openai_api_key and not gemini_api_key:
        print("\n⚠️ CẢNH BÁO: Không tìm thấy API Key nào.")
        print("Vui lòng cung cấp ít nhất OPENAI_API_KEY hoặc GEMINI_API_KEY trong file .env.\n")
        return False
        
    return True
