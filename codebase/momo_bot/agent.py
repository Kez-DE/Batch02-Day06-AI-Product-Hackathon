import json
import os
import logging
from providers.llm_provider import UniversalProvider
from tools import AGENT_TOOLS, TOOL_SCHEMAS

# Cấu hình logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=os.path.join("logs", "ai_agent.log"),
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger("MoniAgent")

class MoniAgent:
    def __init__(self):
        self.provider = UniversalProvider()
        self.system_instruction = self._load_system_prompt()
        self.tools = TOOL_SCHEMAS
        
        # Với OpenAI, chúng ta cần tự duy trì mảng messages
        self.messages = [
            {"role": "system", "content": self.system_instruction}
        ]
        
    def _load_system_prompt(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "artifacts", "system_prompt.md")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def process_message(self, user_message: str):
        """
        Gửi tin nhắn cho LLM và xử lý luồng Function Calling.
        """
        logger.info(f"👤 USER INPUT: {user_message}")
        try:
            self.messages.append({"role": "user", "content": user_message})

            function_map = {tool.__name__: tool for tool in AGENT_TOOLS}

            for _ in range(5):
                response = self.provider.generate_response(
                    messages=self.messages,
                    tools=self.tools
                )

                choice = response.choices[0]
                message = choice.message
                message_dict = message.model_dump(exclude_none=True) if hasattr(message, "model_dump") else dict(message)

                # Lưu lại phản hồi của AI vào lịch sử
                self.messages.append(message_dict)

                # Kiểm tra xem LLM có yêu cầu gọi tool nào không
                if not message.tool_calls:
                    final_response = message.content or "Mình chưa tạo được phản hồi cuối cùng. Bạn thử nói rõ hơn giúp mình nhé."
                    logger.info(f"🤖 AI RESPONSE: {final_response}")
                    return final_response

                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    args_str = tool_call.function.arguments
                    args = json.loads(args_str) if args_str else {}
                    
                    # Log ra terminal để dễ debug (Developer Mode)
                    print(f"\n[🔧 AI ĐANG GỌI TOOL]: {name}({args})")
                    logger.info(f"🔧 TOOL CALL: {name}({args})")
                    
                    if name in function_map:
                        tool_func = function_map[name]
                        # Thực thi tool
                        tool_result = tool_func(**args)
                        logger.info(f"✅ TOOL RESULT: {tool_result}")
                        
                        # Trả lại kết quả của tool cho LLM để nó biết kết quả
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": name,
                            "content": str(tool_result)
                        })

            logger.warning("⚠️ AI chưa chốt được phản hồi sau nhiều bước xử lý.")
            return "Mình đã xử lý nhiều bước nhưng chưa chốt được phản hồi cuối cùng. Bạn thử lại với yêu cầu ngắn hơn nhé."

        except Exception as e:
            logger.error(f"❌ SYSTEM ERROR: {str(e)}")
            return f"❌ [Lỗi Hệ Thống]: {str(e)}"
