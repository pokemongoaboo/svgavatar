import streamlit as st
import requests

def generate_avatar(seed):
    return f"https://api.dicebear.com/6.x/adventurer-neutral/svg?seed={seed}"

st.title("动画头像生成器")

seed = st.text_input("输入一个种子值来生成你的头像:")

if st.button("生成头像"):
    if seed:
        avatar_url = generate_avatar(seed)
        st.image(avatar_url, caption="你的个性化头像", use_column_width=True)
    else:
        st.warning("请输入一个种子值")

st.markdown("""
### 关于这个应用
这个简单的头像生成器使用DiceBear API来创建独特的动画头像。
每个头像都基于你输入的文本种子，所以你可以通过改变种子来获得不同的头像。

尝试输入你的名字、你最喜欢的单词，或任何有趣的短语来看看会生成什么样的头像！
""")
