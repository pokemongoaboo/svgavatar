import streamlit as st
import os
import sys
import cv2
import numpy as np

# 添加PaddleAvatar到系统路径
paddle_avatar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "PaddleAvatar"))
sys.path.append(paddle_avatar_path)

# 导入PaddleAvatar相关模块
from paddleavatar.generate import AvatarGenerator

# 初始化AvatarGenerator
generator = AvatarGenerator()

def main():
    st.title("PaddleAvatar 虚拟人生成器")

    # 上传图片
    uploaded_file = st.file_uploader("上传一张人脸图片", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # 读取上传的图片
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        st.image(image, caption="上传的图片", use_column_width=True)

        # 生成按钮
        if st.button("生成虚拟人"):
            with st.spinner("正在生成虚拟人..."):
                try:
                    # 使用PaddleAvatar生成虚拟人
                    avatar = generator.generate(image)
                    
                    # 显示生成的虚拟人
                    st.image(avatar, caption="生成的虚拟人", use_column_width=True)
                except Exception as e:
                    st.error(f"生成虚拟人时出错: {str(e)}")

if __name__ == "__main__":
    main()
