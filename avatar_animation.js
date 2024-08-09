function drawAnimatedAvatar(avatarUrl, isSpeaking) {
    const canvas = document.getElementById('avatarCanvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    img.src = avatarUrl;
    
    img.onload = function() {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        
        if (isSpeaking) {
            animateMouth();
        }
    }
    
    function animateMouth() {
        let mouthOpenness = 0;
        let increasing = true;
        
        function drawMouth() {
            // 清除嘴巴区域
            ctx.clearRect(80, 110, 40, 30);
            
            // 重绘该区域的头像部分
            ctx.drawImage(img, 80, 110, 40, 30, 80, 110, 40, 30);
            
            // 画嘴巴
            ctx.beginPath();
            ctx.moveTo(90, 125);
            ctx.quadraticCurveTo(100, 125 + mouthOpenness * 10, 110, 125);
            ctx.strokeStyle = 'black';
            ctx.stroke();
            
            // 更新嘴巴开合度
            if (increasing) {
                mouthOpenness += 0.1;
                if (mouthOpenness >= 1) increasing = false;
            } else {
                mouthOpenness -= 0.1;
                if (mouthOpenness <= 0) increasing = true;
            }
            
            requestAnimationFrame(drawMouth);
        }
        
        drawMouth();
    }
}
