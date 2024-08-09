import streamlit as st
from openai import OpenAI
import requests
import json
import time
import websocket
import threading
import base64

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
d_id_api_key = st.secrets["D_ID_API_KEY"]

# Streamlit app
st.title("虛擬對話助理 (實時流式)")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'generating' not in st.session_state:
    st.session_state.generating = False
if 'stream_id' not in st.session_state:
    st.session_state.stream_id = None

# User input and settings
voice_options = ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural", "zh-CN-YunyangNeural"]
selected_voice = st.sidebar.selectbox("選擇語音:", voice_options)

# Function to create D-ID stream
def create_stream():
    url = "https://api.d-id.com/talks/streams"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {d_id_api_key}"
    }
    payload = {
        "source_url": "https://create-images-results.d-id.com/DefaultPresenters/Emma_f/image.png"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Function to stream to D-ID
def stream_to_d_id(stream_id, text):
    url = f"https://api.d-id.com/talks/streams/{stream_id}"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {d_id_api_key}"
    }
    payload = {
        "script": {
            "type": "text",
            "input": text,
            "provider": {
                "type": "microsoft",
                "voice_id": selected_voice
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Function to handle WebSocket connection
def on_message(ws, message):
    data = json.loads(message)
    if 'media' in data:
        image_data = base64.b64decode(data['media']['data'])
        st.image(image_data, use_column_width=True)

def on_error(ws, error):
    st.error(f"WebSocket錯誤: {error}")

def on_close(ws, close_status_code, close_msg):
    st.warning("WebSocket連接已關閉")

def on_open(ws):
    st.success("WebSocket連接已建立")

# Function to connect to WebSocket
def connect_to_websocket(stream_id):
    ws_url = f"wss://api.d-id.com/talks/streams/{stream_id}/connection"
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    return ws

# Function to generate response and stream video
def generate_response_and_stream(user_input):
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

    # Step 2: Stream to D-ID
    if not st.session_state.stream_id:
        stream_data = create_stream()
        st.session_state.stream_id = stream_data['id']
        connect_to_websocket(st.session_state.stream_id)

    try:
        stream_response = stream_to_d_id(st.session_state.stream_id, ai_response)
        if 'error' in stream_response:
            st.error(f"D-ID API錯誤: {stream_response['error']}")
    except Exception as e:
        st.error(f"D-ID API錯誤: {str(e)}")
    
    st.session_state.generating = False

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("請輸入您的問題:")

if user_input and not st.session_state.generating:
    generate_response_and_stream(user_input)

# Display current model information
st.sidebar.write("當前使用的模型: GPT-4")
