import sys
import os
from env_loader import load_env

# Đảm bảo import được thư mục hiện tại
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🔄 Đang khởi tạo Moni Agent...")
    if not load_env():
        return
        
    try:
        from agent import MoniAgent
        agent = MoniAgent()
        print("\n✅ Khởi tạo thành công! Moni đã sẵn sàng.")
        print("💡 Hãy thử gõ: 'Chuyển tiền cho mẹ' hoặc 'Chuyển 100k tới số 0912345678'")
        print("Gõ 'exit' hoặc 'quit' để thoát.\n")
        print("-" * 50)
        
        while True:
            user_input = input("\n👤 Bạn: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Moni chào tạm biệt!")
                break
                
            if not user_input.strip():
                continue
                
            # Đánh dấu đang chờ AI
            print("🤖 Moni đang xử lý...")
            response = agent.process_message(user_input)
            
            print(f"🤖 Moni: {response}")
            
    except Exception as e:
        print(f"\n❌ Lỗi khởi tạo: {str(e)}")
        print("Vui lòng kiểm tra lại cấu hình hoặc API Key.")

if __name__ == "__main__":
    main()
