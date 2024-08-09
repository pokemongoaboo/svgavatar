import streamlit as st
from openai import OpenAI
import requests

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
d_id_api_key = st.secrets["D_ID_API_KEY"]

# Streamlit app
st.title("虛擬對話助理")

# User input
user_input = st.text_input("請輸入您的問題:")

if st.button("獲取回覆"):
    if user_input:
        # Step 1: Get response from OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
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
                "input": ai_response
            },
            "source_url": "https://create-images-results.d-id.com/DefaultPresenters/Emma_f/image.png"
        }
        
        try:
            d_id_response = requests.post(url, json=payload, headers=headers)
            d_id_response.raise_for_status()
            video_url = d_id_response.json()["result_url"]
            st.video(video_url)
            st.write("AI回覆:", ai_response)
        except requests.exceptions.RequestException as e:
            st.error(f"D-ID API錯誤: {str(e)}")
    else:
        st.warning("請輸入問題")

# Display current model information
st.sidebar.write("當前使用的模型: GPT-4")
