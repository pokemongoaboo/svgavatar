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

# User input and settings
user_input = st.text_input("請輸入您的問題:")
voice_options = ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural", "zh-CN-YunyangNeural"]
selected_voice = st.selectbox("選擇語音:", voice_options)
max_duration = st.slider("最大視頻時長 (秒):", 10, 60, 30)

# Function to check video status
def check_video_status(talk_id):
    url = f"https://api.d-id.com/talks/{talk_id}"
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {d_id_api_key}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

if st.button("獲取回覆"):
    if user_input:
        # Step 1: Get response from OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Please respond in Chinese."},
                    {"role": "user", "content": user_input}
                ]
            )
            ai_response = response.choices[0].message.content
        except Exception as e:
            st.error(f"OpenAI API錯誤: {str(e)}")
            st.stop()

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
            "source_url": "https://create-images-results.d-id.com/DefaultPresenters/Emma_f/image.png",
            "webhook": "https://example.com/webhook"
        }
        
        try:
            d_id_response = requests.post(url, json=payload, headers=headers)
            d_id_response.raise_for_status()
            response_data = d_id_response.json()
            
            if "id" in response_data:
                st.session_state['talk_id'] = response_data['id']
                st.success(f"成功創建對話！ID: {response_data['id']}")
                st.info("請點擊 '檢查視頻狀態' 按鈕來查看視頻是否準備就緒。")
            else:
                st.warning("未找到預期的響應數據。請檢查D-ID API文檔以獲取最新的響應格式。")
            
            st.write("AI回覆:", ai_response)
        except requests.exceptions.RequestException as e:
            st.error(f"D-ID API錯誤: {str(e)}")
    else:
        st.warning("請輸入問題")

# Button to check video status
if st.button("檢查視頻狀態") and 'talk_id' in st.session_state:
    talk_id = st.session_state['talk_id']
    status_data = check_video_status(talk_id)
    
    st.write("視頻狀態:", status_data.get('status', 'Unknown'))
    
    if status_data.get('status') == 'done':
        video_url = status_data.get('result_url')
        if video_url:
            st.video(video_url)
        else:
            st.warning("視頻已完成，但未找到URL。")
    elif status_data.get('status') == 'created':
        st.info("視頻正在生成中，請稍後再次檢查。")
    else:
        st.write("完整狀態信息:", json.dumps(status_data, indent=2))

# Display current model information
st.sidebar.write("當前使用的模型: GPT-4")
