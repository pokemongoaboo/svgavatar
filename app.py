import streamlit as st
from openai import OpenAI
import requests
import json

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
d_id_api_key = st.secrets["D_ID_API_KEY"]

# Streamlit app
st.title("虛擬對話助理 (交互式網頁嵌入)")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'generating' not in st.session_state:
    st.session_state.generating = False

# User input and settings
voice_options = ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural", "zh-CN-YunyangNeural"]
selected_voice = st.sidebar.selectbox("選擇語音:", voice_options)

# Function to create D-ID interactive session
def create_interactive_session():
    url = "https://api.d-id.com/talks/streams"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {d_id_api_key}"
    }
    payload = {
        "source_url": "https://create-images-results.d-id.com/DefaultPresenters/Emma_f/image.png",
        "driver_url": "bank://lively/",
        "config": {
            "stitch": True,
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Function to generate response and update interactive session
def generate_response_and_update(user_input):
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

    # Step 2: Update D-ID interactive session
    if 'session_id' not in st.session_state:
        session_data = create_interactive_session()
        st.session_state.session_id = session_data['id']
        st.session_state.iframe_url = session_data['iframe_url']

    try:
        url = f"https://api.d-id.com/talks/streams/{st.session_state.session_id}"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Basic {d_id_api_key}"
        }
        payload = {
            "script": {
                "type": "text",
                "provider": {
                    "type": "microsoft",
                    "voice_id": selected_voice
                },
                "input": ai_response
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            st.error(f"D-ID API錯誤: {response.text}")
    except Exception as e:
        st.error(f"D-ID API錯誤: {str(e)}")
    
    st.session_state.generating = False

# Display interactive iframe
if 'iframe_url' in st.session_state:
    st.components.v1.iframe(st.session_state.iframe_url, height=400)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("請輸入您的問題:")

if user_input and not st.session_state.generating:
    generate_response_and_update(user_input)

# Display current model information
st.sidebar.write("當前使用的模型: GPT-4")
