import streamlit as st
import streamlit.components.v1 as components

# 定義嵌入式HTML
html_code = """
<div id="avatar-container"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    // 這裡添加Three.js代碼來創建和動畫化3D頭像
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(300, 300);
    document.getElementById('avatar-container').appendChild(renderer.domElement);
    
    // 添加一個簡單的立方體作為佔位符
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    
    camera.position.z = 5;
    
    function animate() {
        requestAnimationFrame(animate);
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
        renderer.render(scene, camera);
    }
    animate();
</script>
"""

st.title("Virtual Assistant with 3D Avatar")

# 嵌入HTML
components.html(html_code, height=350)

# 對話框
user_input = st.text_input("你: ")
if user_input:
    # 這裡添加與OpenAI API的集成代碼
    response = "這裡是虛擬助理的回答"
    st.text(f"助理: {response}")
