import streamlit as st
from streamlit_drawable_canvas import st_canvas
import base64

# 簡單的SVG頭像
avatar_svg = """
<svg width="100" height="100" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="45" fill="#4299E1" />
    <circle cx="35" cy="40" r="5" fill="white" />
    <circle cx="65" cy="40" r="5" fill="white" />
    <path d="M 30 60 Q 50 70 70 60" stroke="white" stroke-width="3" fill="none" />
</svg>
"""

# 將SVG轉換為可顯示的格式
b64 = base64.b64encode(avatar_svg.encode("utf-8")).decode("utf-8")

# 顯示頭像
st.write(f'<img src="data:image/svg+xml;base64,{b64}" alt="avatar">', unsafe_allow_html=True)

# 聊天界面
st.title("虛擬助理")

# 初始化聊天歷史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示聊天歷史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用戶輸入
if prompt := st.chat_input("輸入您的訊息..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 這裡你可以添加實際的對話邏輯
    response = f"你說: {prompt}"
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
