import litellm
import os

class UniversalProvider:
    """LiteLLM wrapper hỗ trợ OpenRouter, OpenAI, Gemini với tự động fallback."""

    def __init__(self):
        self.models = []  # list of dict: {model, api_key, api_base}

        openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        openai_key     = os.getenv("OPENAI_API_KEY", "").strip()
        gemini_key     = os.getenv("GEMINI_API_KEY", "").strip()

        # OpenAI — ưu tiên 1 (đã verify hoạt động)
        if openai_key:
            self.models.append({
                "model":    "gpt-4o-mini",
                "api_key":  openai_key,
                "api_base": None,
            })

        # OpenRouter — ưu tiên 2 (cần có credit)
        if openrouter_key:
            self.models.append({
                "model":    "openrouter/google/gemini-2.5-flash",
                "api_key":  openrouter_key,
                "api_base": None,
            })

        # Gemini direct — ưu tiên 3
        if gemini_key:
            self.models.append({
                "model":    "gemini/gemini-2.5-flash",
                "api_key":  gemini_key,
                "api_base": None,
            })

    def generate_response(self, messages: list, tools: list = None):
        if not self.models:
            raise Exception("Không có API Key nào được cấu hình!")

        for cfg in self.models:
            try:
                kwargs = dict(
                    model=cfg["model"],
                    messages=messages,
                    tools=tools if tools else None,
                    temperature=0.0,
                    api_key=cfg["api_key"],
                )
                if cfg["api_base"]:
                    kwargs["api_base"] = cfg["api_base"]

                response = litellm.completion(**kwargs)
                print(f"⚡ [Model]: {cfg['model']}")
                return response

            except Exception as e:
                print(f"\n⚠️ [CẢNH BÁO]: Model {cfg['model']} thất bại "
                      f"(Lý do: {str(e)[:120]}). Đang thử model tiếp theo...")
                continue

        raise Exception("Tất cả các model đều bị lỗi hoặc hết hạn mức!")
