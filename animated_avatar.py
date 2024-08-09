import streamlit.components.v1 as components
import streamlit as st

def animated_avatar(avatar_url, is_speaking=False):
    # 读取JS代码
    with open('avatar_animation.js', 'r') as file:
        js_code = file.read()
    
    # 创建HTML，包含Canvas和JS代码
    html = f"""
    <canvas id="avatarCanvas" width="200" height="200"></canvas>
    <script>
    {js_code}
    </script>
    <script>
    drawAnimatedAvatar("{avatar_url}", {str(is_speaking).lower()});
    </script>
    """
    
    # 使用Streamlit组件来渲染HTML
    components.html(html, height=220)
