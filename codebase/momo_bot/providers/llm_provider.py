import litellm
import os

class UniversalProvider:
    """Wrapper class sử dụng LiteLLM để tự động Fallback (Dự phòng) giữa OpenAI và Gemini."""
    
    def __init__(self):
        # Danh sách mô hình theo thứ tự ưu tiên. Nếu cái 1 lỗi (hết hạn mức), sẽ tự nhảy sang cái 2.
        self.models = []
        if os.getenv("OPENAI_API_KEY"):
            self.models.append("gpt-4o-mini")
        if os.getenv("GEMINI_API_KEY"):
            self.models.append("gemini/gemini-2.5-flash")
            
    def generate_response(self, messages: list, tools: list = None):
        """
        Gửi message tới LLM, tự động chuyển đổi mô hình nếu gặp lỗi (Rate Limit).
        """
        if not self.models:
            raise Exception("Không có API Key nào được cấu hình!")
            
        for model in self.models:
            try:
                # Trích xuất đúng API Key tương ứng với model và loại bỏ khoảng trắng thừa
                api_key = os.getenv("OPENAI_API_KEY") if "gpt" in model else os.getenv("GEMINI_API_KEY")
                if api_key:
                    api_key = api_key.strip()
                    
                response = litellm.completion(
                    model=model,
                    messages=messages,
                    tools=tools if tools else None,
                    temperature=0.0,
                    api_key=api_key
                )
                print(f"⚡ [Đã dùng model]: {model}")
                return response
            except Exception as e:
                print(f"\n⚠️ [CẢNH BÁO]: Model {model} thất bại (Lý do: {str(e)}). Đang chuyển sang model dự phòng...")
                continue
                
        raise Exception("Tất cả các LLM đều bị lỗi hoặc đã hết hạn mức!")
