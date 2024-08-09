import streamlit as st
import time
from gtts import gTTS
import os
import base64
from animated_avatar import animated_avatar

def text_to_speech(text, lang='zh-cn'):
    tts = gTTS(text=text, lang=lang)
    tts.save("speech.mp3")
    with open("speech.mp3", "rb") as f:
        audio_bytes = f.read()
    os.remove("speech.mp3")
    return audio_bytes

def main():
    st.title("虚拟助理")

    avatar_seed = st.text_input("输入头像种子:", value="assistant")
    message = st.text_input("输入消息:")

    if st.button("说话"):
        avatar_url = f"https://api.dicebear.com/6.x/adventurer-neutral/svg?seed={avatar_seed}"
        
        # 使用自定义动画组件
        animated_avatar(avatar_url, is_speaking=True)
        
        audio_bytes = text_to_speech(message)
        st.audio(audio_bytes, format='audio/mp3')
        
        # 等待音频播放完毕（这里假设每个字需要0.5秒）
        time.sleep(len(message) * 0.5)
        
        # 停止说话动画
        animated_avatar(avatar_url, is_speaking=False)

    st.markdown("""
    ### 关于这个应用
    这个虚拟助理应用使用DiceBear API生成头像，使用自定义的Canvas动画来模拟说话效果，并使用gTTS（Google Text-to-Speech）生成语音。
    """)

if __name__ == "__main__":
    main()
