import streamlit as st
import sys, os, json, re
import base64, mimetypes
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parents[1]
TRANSFER_UI_DIR = PROJECT_ROOT / "transfer_UI"


def query_param_is(name: str, expected: str) -> bool:
    value = st.query_params.get(name)
    if isinstance(value, list):
        return expected in value
    return value == expected


def query_param_value(name: str, default: str = "") -> str:
    value = st.query_params.get(name)
    if isinstance(value, list):
        return value[0] if value else default
    return value or default

st.set_page_config(
    page_title="Trợ thủ AI – Moni",
    page_icon="💜",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  DESIGN SYSTEM  —  Dựa theo ảnh chụp thực tế MoMo Moni
#
#  BG     : gradient #FAFAFE → #EDE8FF → #E3D8FF  (lavender nhẹ)
#  User   : #F02891  (hot pink MoMo)
#  Bot    : #FFFFFF  (trắng, shadow nhẹ)
#  Input  : white pill, sparkle ✦ icon
#  Accent : #F02891
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');

/* ─── Reset ─────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], [class*="st-"], button, input, textarea {
    font-family: 'Be Vietnam Pro', -apple-system, sans-serif !important;
}

/* ─── Ẩn chrome Streamlit ───────────────────────────────────── */
[data-testid="stHeader"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
footer { display: none !important; }

/* ─── App background — lavender gradient như MoMo ───────────── */
.stApp {
    background: linear-gradient(170deg,
        #FAFAFE 0%,
        #F3F0FF 30%,
        #EDE8FF 65%,
        #E3D8FF 100%) !important;
    min-height: 100vh;
}
.block-container {
    padding: 0 !important;
    max-width: 680px !important;
    background: transparent !important;
}

/* ─── Sidebar — frosted glass, blend với gradient ───────────── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.82) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(200,180,240,0.25) !important;
}
[data-testid="stSidebar"] section[data-testid="stSidebarContent"] {
    padding: 20px 16px !important;
}
[data-testid="stSidebar"],
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label { color: #2D2D4E !important; }
[data-testid="stSidebar"] h3 {
    color: #8B5CF6 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: .09em !important;
    margin: 18px 0 8px !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li { font-size: 13px !important; color: #4A4A6A !important; }
[data-testid="stSidebar"] strong { color: #1A1A3E !important; }
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(140,92,246,.15) !important;
    margin: 14px 0 !important;
}
[data-testid="stSidebar"] [data-testid="stCaption"] { color: #9B9BB4 !important; font-size: 11px !important; }

/* Sidebar: new chat button */
[data-testid="stSidebar"] button[kind="primary"] {
    background: #F02891 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 50px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 18px !important;
    box-shadow: 0 4px 14px rgba(240,40,145,.3) !important;
    transition: all .2s !important;
}
[data-testid="stSidebar"] button[kind="primary"]:hover {
    background: #C4197A !important;
    box-shadow: 0 6px 18px rgba(240,40,145,.4) !important;
    transform: translateY(-1px) !important;
}

/* ─── Text màu tối trong main ───────────────────────────────── */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span { color: #1A1A3E !important; }

/* ═══════════════════════════════════════════════════════════════
   CHAT MESSAGES  —  Giống hệt ảnh MoMo
═══════════════════════════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    background: transparent !important;
    box-shadow: none !important;
    padding: 3px 16px !important;
    gap: 10px !important;
}

/* Bot bubble — trắng, shadow mềm */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"])
  [data-testid="stChatMessageContent"] {
    background: #FFFFFF !important;
    border-radius: 4px 20px 20px 20px !important;
    padding: 14px 18px !important;
    color: #1A1A3E !important;
    box-shadow: 0 2px 14px rgba(100,60,200,.1) !important;
    border: none !important;
    max-width: 85% !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"])
  [data-testid="stChatMessageContent"] p {
    color: #1A1A3E !important;
    font-size: 14.5px !important;
    line-height: 1.65 !important;
}

/* User bubble — hot pink pill, giống MoMo */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"])
  [data-testid="stChatMessageContent"] {
    background: #F02891 !important;
    border-radius: 20px 20px 4px 20px !important;
    padding: 13px 18px !important;
    color: #fff !important;
    box-shadow: 0 4px 16px rgba(240,40,145,.35) !important;
    border: none !important;
    max-width: 82% !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"])
  [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"])
  [data-testid="stChatMessageContent"] span {
    color: #FFFFFF !important;
    font-size: 14.5px !important;
    line-height: 1.65 !important;
}

/* ═══════════════════════════════════════════════════════════════
   SUGGESTION BUTTONS  —  Card trắng, bo tròn
═══════════════════════════════════════════════════════════════ */
div[data-testid="stButton"] > button[kind="secondary"] {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(200,180,240,.35) !important;
    color: #3D2B7A !important;
    border-radius: 16px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 14px 14px !important;
    text-align: left !important;
    line-height: 1.45 !important;
    transition: all .18s ease !important;
    box-shadow: 0 2px 10px rgba(100,60,200,.08) !important;
    backdrop-filter: blur(8px) !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: #FFFFFF !important;
    border-color: #F02891 !important;
    color: #F02891 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(240,40,145,.15) !important;
}

/* ═══════════════════════════════════════════════════════════════
   BOTTOM INPUT BAR  —  trong suốt, pill trắng như MoMo
═══════════════════════════════════════════════════════════════ */

/* Xóa nền đen hoàn toàn — mọi wrapper quanh input */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div,
[data-testid="stBottom"] > div > div > div,
section[data-testid="stBottom"],
div[data-testid="stBottom"],
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div,
.stBottom, .stBottom > div,
/* Streamlit đôi khi dùng class này */
.st-emotion-cache-1c7y2kd,
.st-emotion-cache-6q9sum,
[class*="stChatInput"] {
    background: transparent !important;
    background-color: transparent !important;
    border-top: none !important;
    box-shadow: none !important;
}

/* Pill ngoài — trắng */
[data-testid="stChatInput"] > div,
.stChatInput > div {
    background: rgba(255,255,255,0.95) !important;
    border: 1.5px solid rgba(200,180,240,.45) !important;
    border-radius: 50px !important;
    box-shadow: 0 4px 24px rgba(100,60,200,.12) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stChatInput"] > div:focus-within,
.stChatInput > div:focus-within {
    border-color: #F02891 !important;
    box-shadow: 0 4px 28px rgba(240,40,145,.2) !important;
}

/* Tất cả div con bên trong pill → transparent */
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] > div > div > div,
[data-testid="stChatInput"] > div > div > div > div,
.stChatInput > div > div,
.stChatInput > div > div > div {
    background: transparent !important;
    background-color: transparent !important;
}

/* :has() — target div CHA của textarea trực tiếp */
div:has(> [data-testid="stChatInputTextArea"]),
div:has(> [data-testid="stChatInputTextArea"]) > div {
    background: transparent !important;
    background-color: transparent !important;
}

/* Tăng specificity cao nhất có thể */
html body div[data-testid="stChatInputTextArea"],
html body textarea[data-testid="stChatInputTextArea"] {
    background: transparent !important;
    background-color: transparent !important;
    color: #2D2D4E !important;
}

/* Textarea — target chính xác data-testid */
[data-testid="stChatInputTextArea"],
[data-testid="stChatInput"] textarea,
.stChatInput textarea,
textarea[data-testid="stChatInputTextArea"] {
    background: transparent !important;
    background-color: transparent !important;
    color: #2D2D4E !important;
    caret-color: #F02891 !important;
    font-size: 14px !important;
    font-family: 'Be Vietnam Pro', sans-serif !important;
    padding: 12px 16px !important;
    border: none !important;
    box-shadow: none !important;
}
[data-testid="stChatInputTextArea"]::placeholder {
    color: #A89FC8 !important;
    font-size: 14px !important;
}
/* Parent trực tiếp của textarea cũng phải transparent */
[data-testid="stChatInputTextArea"]:is(textarea) {
    background-color: transparent !important;
}
/* Override các st-* class của Streamlit */
[data-testid="stChatInputTextArea"][class] {
    background: transparent !important;
    background-color: transparent !important;
}

/* Nút gửi — hồng tròn */
[data-testid="stChatInput"] button,
.stChatInput button {
    background: linear-gradient(135deg, #F02891, #8B5CF6) !important;
    border-radius: 50% !important;
    border: none !important;
    margin: 6px !important;
    box-shadow: 0 3px 12px rgba(240,40,145,.4) !important;
    transition: all .2s !important;
}
[data-testid="stChatInput"] button:hover,
.stChatInput button:hover {
    opacity: .88 !important;
    transform: scale(1.07) !important;
}
[data-testid="stChatInput"] button svg path,
.stChatInput button svg path { fill: #fff !important; }

/* ─── Spinner ───────────────────────────────────────────────── */
[data-testid="stSpinner"] div { border-top-color: #F02891 !important; }

/* ─── Expander ──────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,.7) !important;
    border: 1px solid rgba(200,180,240,.3) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(8px) !important;
}
[data-testid="stExpander"] summary { color: #9B9BB4 !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER  —  Tối giản như MoMo mobile
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="
    padding: 14px 20px 10px;
    display: flex; align-items: center; gap: 12px;
    background: transparent;
">
  <!-- Moni avatar — pink circle với face -->
  <div style="
      width: 40px; height: 40px; flex-shrink: 0;
      background: linear-gradient(135deg, #F02891 0%, #C4197A 100%);
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px;
      box-shadow: 0 4px 12px rgba(240,40,145,.3);
  ">✨</div>

  <div style="flex:1;">
    <div style="font-size:15px; font-weight:700; color:#1A1A3E; letter-spacing:-.01em;">
      Trợ thủ AI – Moni
    </div>
    <div style="
        font-size:11px; color:#9B9BB4; margin-top:1px;
        display:flex; align-items:center; gap:5px;
    ">
      <span style="
          width:5px; height:5px; background:#4ADE80; border-radius:50%;
          animation: moniPulse 2s infinite;
      "></span>
      Đang hoạt động
    </div>
  </div>
</div>
<style>@keyframes moniPulse{0%,100%{opacity:1}50%{opacity:.35}}</style>
""", unsafe_allow_html=True)



# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
<div style="
    display:flex; align-items:center; gap:10px;
    padding:4px 0 16px;
    border-bottom:1px solid rgba(140,92,246,.12);
    margin-bottom:4px;
">
  <div style="
      width:36px; height:36px; flex-shrink:0;
      background:linear-gradient(135deg,#F02891,#8B5CF6);
      border-radius:10px;
      display:flex;align-items:center;justify-content:center;
      font-size:18px;
      box-shadow:0 4px 12px rgba(240,40,145,.3);
  ">✨</div>
  <div>
    <div style="font-size:14px;font-weight:700;color:#1A1A3E;">Moni</div>
    <div style="font-size:10px;color:#9B9BB4;">Trợ thủ AI · MoMo</div>
  </div>
</div>
""", unsafe_allow_html=True)

    if st.button("＋  Cuộc trò chuyện mới", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.pending_deeplink = None
        if "agent" in st.session_state:
            del st.session_state["agent"]
        st.rerun()

    st.markdown("### Moni làm được gì?")
    sb_card = "background:rgba(240,40,145,.06);border:1px solid rgba(240,40,145,.15);border-radius:10px;padding:10px 12px;display:flex;align-items:flex-start;gap:9px;margin-bottom:6px;"
    sb_icon = "font-size:16px;margin-top:1px;"
    sb_title = "font-size:12px;font-weight:600;color:#1A1A3E;"
    sb_sub = "font-size:11px;color:#6B6B8F;margin-top:1px;"
    st.markdown(f"""
<div>
<div style="{sb_card}"><span style="{sb_icon}">💸</span><div><div style="{sb_title}">Chuyển tiền</div><div style="{sb_sub}">Theo SĐT hoặc tên danh bạ</div></div></div>
<div style="{sb_card}"><span style="{sb_icon}">🔒</span><div><div style="{sb_title}">Kiểm tra an toàn</div><div style="{sb_sub}">Tự động trước mỗi giao dịch</div></div></div>
<div style="{sb_card}"><span style="{sb_icon}">👥</span><div><div style="{sb_title}">Tìm liên hệ</div><div style="{sb_sub}">Có dấu hoặc không dấu</div></div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### Thử ngay")
    st.markdown("""
<div style="display:flex;flex-direction:column;gap:5px;">
  <div style="background:rgba(240,40,145,.07);border:1px solid rgba(240,40,145,.2);
      border-radius:8px;padding:7px 11px;font-size:12px;color:#C4197A;">
    💬 "Chuyển 100k cho mẹ"
  </div>
  <div style="background:rgba(240,40,145,.07);border:1px solid rgba(240,40,145,.2);
      border-radius:8px;padding:7px 11px;font-size:12px;color:#C4197A;">
    💬 "Gửi 50k tới 0912345678"
  </div>
  <div style="background:rgba(240,40,145,.07);border:1px solid rgba(240,40,145,.2);
      border-radius:8px;padding:7px 11px;font-size:12px;color:#C4197A;">
    💬 "Chuyển tiền cho anh Hùng"
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Moni v1.0 · Powered by AI")


# ═══════════════════════════════════════════════════════════════════════════════
#  INIT
# ═══════════════════════════════════════════════════════════════════════════════
from env_loader import load_env
from agent import MoniAgent

if "initialized" not in st.session_state:
    st.session_state.initialized = load_env()
if st.session_state.get("initialized") and "agent" not in st.session_state:
    st.session_state.agent = MoniAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_deeplink" not in st.session_state:
    st.session_state.pending_deeplink = None

if query_param_is("transfer_done", "1"):
    st.session_state.messages = []
    st.session_state.pending_deeplink = None
    if "agent" in st.session_state:
        del st.session_state["agent"]
    st.query_params.clear()
    st.rerun()

if not st.session_state.get("initialized"):
    st.markdown("""
<div style="margin:20px;background:rgba(255,255,255,.85);
    border:1px solid rgba(234,179,8,.4);border-left:4px solid #EAB308;
    border-radius:14px;padding:16px 18px;font-size:14px;color:#713F12;
    backdrop-filter:blur(12px);">
  <b>⚠️ Chưa cấu hình API Key</b><br>
  Vui lòng điền key vào <code style="background:#FEF08A;padding:1px 5px;border-radius:4px;">
  momo_bot/.env</code> rồi khởi động lại.
</div>
""", unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def get_last_deeplink(agent: MoniAgent) -> dict | None:
    for msg in reversed(agent.messages):
        if (isinstance(msg, dict)
                and msg.get("role") == "tool"
                and msg.get("name") == "execute_momo_transfer"):
            try:
                r = json.loads(msg["content"])
                if r.get("action") == "trigger_deeplink":
                    return r
            except Exception:
                pass
    return None


def extract_transfer_params(data: dict) -> dict:
    deeplink = data.get("deeplink", "")
    phone_match = re.search(r"phone=([^&]+)", deeplink)
    amount_match = re.search(r"amount=(\d+)", deeplink)
    return {
        "name": data.get("recipient_name") or data.get("name") or "Someone",
        "phone": data.get("phone_number") or data.get("phone") or (phone_match.group(1) if phone_match else "09xxxxxxxx"),
        "amount": str(data.get("amount") or (amount_match.group(1) if amount_match else "")),
    }


def open_transfer_flow(data: dict):
    params = extract_transfer_params(data)
    st.query_params.clear()
    st.query_params["transfer"] = "1"
    st.query_params["name"] = params["name"]
    st.query_params["phone"] = params["phone"]
    if params["amount"]:
        st.query_params["amount"] = params["amount"]
    st.rerun()


def transfer_flow_url(data: dict) -> str:
    params = extract_transfer_params(data)
    query = {
        "transfer": "1",
        "name": params["name"],
        "phone": params["phone"],
    }
    if params["amount"]:
        query["amount"] = params["amount"]
    return "?" + urlencode(query)


def _asset_data_uri(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def render_transfer_flow(data: dict):
    if not TRANSFER_UI_DIR.exists():
        st.error("Không tìm thấy giao diện transfer_UI.")
        return

    index_path = TRANSFER_UI_DIR / "index.html"
    css_path = TRANSFER_UI_DIR / "css" / "main.css"
    html = index_path.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")

    def inline_css_asset(match: re.Match) -> str:
        asset_path = (css_path.parent / match.group(1)).resolve()
        if not asset_path.exists():
            return "none"
        return f'url("{_asset_data_uri(asset_path)}")'

    css = re.sub(r'url\(["\']?(\.\./images/[^)"\']+)["\']?\)', inline_css_asset, css)
    html = re.sub(
        r'<link href="\./css/main\.css" rel="stylesheet"\s*/?>',
        f"<style>{css}</style>",
        html,
    )

    params = extract_transfer_params(data)
    phone = params["phone"]
    amount = f"{int(params['amount']):,}d" if params["amount"].isdigit() else ""
    recipient_name = params["name"]

    html = html.replace("09xxxxxxxx", phone)
    html = html.replace("Someone", recipient_name)
    if amount:
        html = html.replace("50.000d", amount, 1)

    html = re.sub(r"</?(?:!doctype|html|head|body)[^>]*>", "", html, flags=re.IGNORECASE)
    html = html.replace("<title>Document</title>", "")

    st.markdown(html, unsafe_allow_html=True)
    st.markdown('<div style="padding:12px 18px 28px;">', unsafe_allow_html=True)
    if st.button("Hoàn thành giao dịch", key="complete_transfer", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_deeplink = None
        if "agent" in st.session_state:
            del st.session_state["agent"]
        st.query_params.clear()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_deeplink_card(data: dict):
    deeplink = data.get("deeplink", "")
    name     = data.get("recipient_name", "người nhận")
    m        = re.search(r"amount=(\d+)", deeplink)
    amount   = f"{int(m.group(1)):,}đ" if m else ""
    transfer_url = transfer_flow_url(data)

    st.markdown(f"""
<div style="
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(200,180,240,.35);
    border-radius: 20px;
    overflow: hidden;
    margin: 10px 0 4px;
    box-shadow: 0 8px 28px rgba(100,60,200,.12);
    backdrop-filter: blur(16px);
">
  <!-- Strip hồng trên cùng -->
  <div style="
      background: linear-gradient(135deg,#F02891 0%,#8B5CF6 100%);
      padding: 16px 20px;
      display: flex; align-items: center; gap: 13px;
  ">
    <div style="
        width:42px;height:42px;flex-shrink:0;
        background:rgba(255,255,255,.2);
        border:1.5px solid rgba(255,255,255,.45);
        border-radius:50%;
        display:flex;align-items:center;justify-content:center;
        font-size:20px;
    ">✅</div>
    <div>
      <div style="font-size:15px;font-weight:700;color:#fff;letter-spacing:-.01em;">
        Sẵn sàng chuyển tiền
      </div>
      <div style="font-size:12.5px;color:rgba(255,255,255,.8);margin-top:3px;">
        Tới: <b style="color:#fff;">{name}</b>
        {"&nbsp;·&nbsp;<b style='color:#fff;'>" + amount + "</b>" if amount else ""}
      </div>
    </div>
  </div>

  <!-- Body -->
  <div style="padding:16px 20px 18px;">
    <a href="{transfer_url}" target="_self" style="
        display:flex;align-items:center;justify-content:center;gap:8px;
        background:linear-gradient(135deg,#F02891,#8B5CF6);
        color:#fff;text-decoration:none;
        padding:14px 20px;border-radius:50px;
        font-weight:700;font-size:14.5px;
        box-shadow:0 6px 18px rgba(240,40,145,.35);
        letter-spacing:.01em;
    ">
      🚀&nbsp; Mở ứng dụng MoMo
    </a>
    <div style="text-align:center;margin-top:10px;font-size:11.5px;color:#A89FC8;">
      Bạn sẽ được chuyển sang MoMo để xác nhận giao dịch
    </div>
  </div>
</div>
""", unsafe_allow_html=True)



def render_warning(text: str):
    st.markdown(f"""
<div style="
    background:rgba(254,243,199,.85);
    border:1px solid rgba(251,191,36,.4);border-left:3px solid #F59E0B;
    border-radius:12px;padding:11px 15px;
    margin:6px 0;font-size:13px;line-height:1.55;color:#78350F;
    display:flex;gap:8px;align-items:flex-start;
    backdrop-filter:blur(8px);
">
  <span style="font-size:15px;flex-shrink:0;margin-top:1px;">⚠️</span>
  <span>{text}</span>
</div>
""", unsafe_allow_html=True)


def get_current_transfer_payload() -> dict | None:
    if query_param_is("transfer", "1"):
        return {
            "name": query_param_value("name", "Someone"),
            "phone": query_param_value("phone", "09xxxxxxxx"),
            "amount": query_param_value("amount"),
        }
    if st.session_state.pending_deeplink:
        return st.session_state.pending_deeplink
    for msg in reversed(st.session_state.messages):
        if msg.get("deeplink"):
            return msg["deeplink"]
    return None


if query_param_is("transfer", "1"):
    transfer_payload = get_current_transfer_payload()
    if transfer_payload:
        render_transfer_flow(transfer_payload)
    else:
        st.warning("Chưa có giao dịch chuyển tiền để hiển thị.")
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
#  WELCOME SCREEN  —  Như màn hình MoMo Moni
# ═══════════════════════════════════════════════════════════════════════════════
SUGGESTIONS = [
    ("💸", "Chuyển 50k cho mẹ", "Chuyển tiền nhanh cho người thân"),
    ("📲", "Gửi 100.000đ tới\n0912345678", "Chuyển theo số điện thoại"),
    ("👤", "Chuyển tiền cho\nanh Hùng", "Tìm trong danh bạ MoMo"),
    ("⚡", "Chuyển 200k cho\nbạn Lan", "Kiểm tra an toàn tự động"),
]

st.markdown('<div style="padding:0 16px 100px;">', unsafe_allow_html=True)

col_greet, col_new = st.columns([3, 1])
with col_new:
    st.markdown('<div style="padding-top:14px;">', unsafe_allow_html=True)
    if st.button("＋ Cuộc trò chuyện mới", key="new_chat_btn", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_deeplink = None
        if "agent" in st.session_state:
            del st.session_state["agent"]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.messages:
    with col_greet:
        st.markdown("""
<div style="padding:10px 4px 24px; display:flex; align-items:flex-start; gap:14px;">
  <div style="
      width:48px; height:48px; flex-shrink:0;
      background:linear-gradient(135deg,#F02891 0%,#8B5CF6 100%);
      border-radius:50%;
      display:flex;align-items:center;justify-content:center;
      font-size:24px;
      box-shadow:0 6px 18px rgba(240,40,145,.3);
  ">✨</div>
  <div style="padding-top:4px;">
    <div style="font-size:22px;font-weight:700;color:#1A1A3E;line-height:1.35;letter-spacing:-.02em;">
      Chào bạn! Moni<br>có thể giúp gì cho bạn?
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # "Mọi người thường hỏi gì?" section label
    st.markdown("""
<div style="
    font-size:12px;font-weight:600;color:#9B9BB4;
    text-transform:uppercase;letter-spacing:.08em;
    margin:0 0 10px 4px;
">Gợi ý dành cho bạn</div>
""", unsafe_allow_html=True)

    # Suggestion cards — 2 cột
    c1, c2 = st.columns(2, gap="small")
    for i, (emoji, label, desc) in enumerate(SUGGESTIONS):
        # Hiển thị label 1 dòng (bỏ newline khi truyền vào button)
        btn_label = f"{emoji}  {label.replace(chr(10), ' ')}"
        with (c1 if i % 2 == 0 else c2):
            if st.button(btn_label, key=f"sug_{i}", use_container_width=True):
                # Chỉ lấy phần text chính (không có emoji)
                clean = label.replace(chr(10), ' ').strip()
                st.session_state["_pending"] = clean
                st.rerun()

    # "Tính năng nổi bật" — style gộp 1 dòng tránh Markdown hiểu là code block
    card_style = "background:rgba(255,255,255,.88);border:1px solid rgba(200,180,240,.3);border-radius:16px;padding:14px 12px;backdrop-filter:blur(12px);box-shadow:0 2px 12px rgba(100,60,200,.08);"
    icon_style = "font-size:22px;margin-bottom:8px;"
    text_style = "font-size:12px;font-weight:600;color:#1A1A3E;line-height:1.4;"

    st.markdown(f"""
<div style="margin:20px 0 0;">
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
<div style="font-size:13px;font-weight:600;color:#2D2D4E;">Tính năng nổi bật</div>
<div style="font-size:12px;color:#F02891;font-weight:500;cursor:pointer;">Xem thêm</div>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
<div style="{card_style}"><div style="{icon_style}">⚡</div><div style="{text_style}">Mẹo quản lý chi tiêu dưới 1 phút/ngày</div></div>
<div style="{card_style}"><div style="{icon_style}">💸</div><div style="{text_style}">Chuyển tiền nhanh &amp; an toàn</div></div>
<div style="{card_style}"><div style="{icon_style}">🔒</div><div style="{text_style}">Khoản chi bất thường gần đây</div></div>
</div>
</div>
""", unsafe_allow_html=True)

# ─── Chat history ─────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("deeplink"):
            render_deeplink_card(msg["deeplink"])

st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  INPUT  —  "✦ Hỏi Moni bất cứ điều gì..."
# ═══════════════════════════════════════════════════════════════════════════════
pending      = st.session_state.pop("_pending", None)
user_input   = st.chat_input("✦  Hỏi Moni bất cứ điều gì...")
message_text = user_input or pending

if message_text:
    st.session_state.messages.append({"role": "user", "content": message_text})
    deeplink_data = None
    with st.chat_message("user", avatar="🧑"):
        st.markdown(message_text)

    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Moni đang xử lý..."):
            agent: MoniAgent = st.session_state.agent
            response = agent.process_message(message_text)

        st.markdown(response)

        deeplink_data = get_last_deeplink(agent)
        if deeplink_data:
            st.session_state.pending_deeplink = deeplink_data
            st.info("Đang mở giao diện chuyển tiền...")

        warning_kw = ["cảnh báo", "danh sách đen", "lừa đảo", "bị khóa", "rủi ro cao"]
        if any(kw in response.lower() for kw in warning_kw):
            render_warning("Giao dịch có dấu hiệu bất thường. Vui lòng kiểm tra kỹ trước khi tiếp tục.")

    record = {"role": "assistant", "content": response}
    if deeplink_data:
        record["deeplink"] = deeplink_data
    st.session_state.messages.append(record)
    if deeplink_data:
        open_transfer_flow(deeplink_data)
