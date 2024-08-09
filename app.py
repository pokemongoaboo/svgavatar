import streamlit as st
import time

def generate_avatar_url(seed, style):
    return f"https://api.dicebear.com/6.x/{style}/svg?seed={seed}"

st.title("动画头像生成器")

seed = st.text_input("输入一个基础种子值来生成你的动画头像:")
style = st.selectbox("选择头像风格", ["adventurer", "avataaars", "bottts", "pixel-art"])

if st.button("生成动画头像"):
    if seed:
        frames = 5
        placeholder = st.empty()
        while True:
            for i in range(frames):
                avatar_url = generate_avatar_url(f"{seed}{i}", style)
                placeholder.image(avatar_url, caption="你的动画头像", use_column_width=True)
                time.sleep(0.2)
    else:
        st.warning("请输入一个种子值")

st.markdown("""
### 关于这个应用
这个动画头像生成器使用DiceBear API创建一系列稍有不同的头像，然后快速切换它们来创造动画效果。
尝试不同的种子值和头像风格来创建你自己的独特动画头像！
""")
