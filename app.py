import streamlit as st
from openai import OpenAI
import requests
import json
import time

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
d_id_api_key = st.secrets["D_ID_API_KEY"]

# Streamlit app
st.title("虛擬對話助理")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'generating' not in st.session_state:
    st.session_state.generating = False

# User input and settings
voice_options = ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural", "zh-CN-YunyangNeural"]
selected_voice = st.sidebar.selectbox("選擇語音:", voice_options)
max_duration = st.sidebar.slider("最大視頻時長 (秒):", 10, 60, 30)

# Function to check video status
def check_video_status(talk_id):
    url = f"https://api.d-id.com/talks/{talk_id}"
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {d_id_api_key}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Function to display auto-playing video
def display_auto_play_video(video_url):
    video_html = f"""
        <div style="width:100%; max-width:600px; margin:auto;">
            <video width="100%" autoplay playsinline>
                <source src="{video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <script>
            var video = document.querySelector('video');
            video.muted = false;
            var playPromise = video.play();
            if (playPromise !== undefined) {{
                playPromise.then(_ => {{
                    console.log('Autoplay started');
                }}).catch(error => {{
                    console.log('Autoplay was prevented');
                    // Show a "Play" button so that user can start playback manually.
                    var playButton = document.createElement('button');
                    playButton.innerHTML = "播放視頻";
                    playButton.onclick = function() {{
                        video.play();
                        this.style.display = 'none';
                    }};
                    video.parentNode.insertBefore(playButton, video.nextSibling);
                }});
            }}
        </script>
    """
    st.components.v1.html(video_html, height=400)

# Function to generate response and video
def generate_response_and_video(user_input):
    st.session_state.generating = True
    
    # Step 1: Get response from OpenAI
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Please respond in Chinese."},
            *st.session_state.messages,
            {"role": "user", "content": user_input}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        ai_response = response.choices[0].message.content
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
    except Exception as e:
        st.error(f"OpenAI API錯誤: {str(e)}")
        st.session_state.generating = False
        return

    # Step 2: Generate video using D-ID
    url = "https://api.d-id.com/talks"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {d_id_api_key}"
    }
    payload = {
        "script": {
            "type": "text",
            "input": ai_response,
            "provider": {
                "type": "microsoft",
                "voice_id": selected_voice
            }
        },
        "config": {
            "fluent": True,
            "pad_audio": 0,
            "driver_expressions": {
                "expressions": [{"expression": "neutral", "start_frame": 0, "intensity": 0.7}]
            }
        },
        "source_url": "https://create-images-results.d-id.com/DefaultPresenters/Emma_f/image.png"
    }
    
    try:
        d_id_response = requests.post(url, json=payload, headers=headers)
        d_id_response.raise_for_status()
        response_data = d_id_response.json()
        
        if "id" in response_data:
            talk_id = response_data['id']
            
            # Wait for video to be ready
            for _ in range(30):  # Try for 30 seconds
                status_data = check_video_status(talk_id)
                if status_data.get('status') == 'done':
                    video_url = status_data.get('result_url')
                    if video_url:
                        display_auto_play_video(video_url)
                        break
                time.sleep(1)
            else:
                st.warning("視頻生成超時，請稍後再試。")
        else:
            st.warning("未找到預期的響應數據。請檢查D-ID API文檔以獲取最新的響應格式。")
        
    except requests.exceptions.RequestException as e:
        st.error(f"D-ID API錯誤: {str(e)}")
    
    st.session_state.generating = False

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("請輸入您的問題:")

if user_input and not st.session_state.generating:
    generate_response_and_video(user_input)

# Display current model information
st.sidebar.write("當前使用的模型: GPT-4")
