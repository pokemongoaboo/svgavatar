import streamlit as st
import time
from gtts import gTTS
import os
import base64

def text_to_speech(text, lang='zh-cn'):
    tts = gTTS(text=text, lang=lang)
    tts.save("speech.mp3")
    with open("speech.mp3", "rb") as f:
        audio_bytes = f.read()
    os.remove("speech.mp3")
    return audio_bytes

st.title("虚拟助理")

avatar_seed = st.text_input("输入头像种子:", value="assistant")
message = st.text_input("输入消息:")

if st.button("说话"):
    avatar_url = f"https://api.dicebear.com/6.x/adventurer-neutral/svg?seed={avatar_seed}"
    st.image(avatar_url, width=200)
    
    audio_bytes = text_to_speech(message)
    st.audio(audio_bytes, format='audio/mp3')
    
    # 模拟嘴巴动画
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)

st.markdown("""
### 关于这个应用
这个虚拟助理应用使用DiceBear API生成头像，并使用gTTS（Google Text-to-Speech）生成语音。
嘴巴动画目前是用进度条模拟的。在实际应用中，你可能需要使用更高级的动画技术。
""")
