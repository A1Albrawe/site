import os
from flask import Blueprint, render_template_string, current_app

snake_blueprint = Blueprint('snake', __name__)

SNAKE_TERMINAL_CSS = """
<style>
    :root {
        --bg-global: #020406; --text-main: #3fb950; --bg-card: rgba(6, 10, 15, 0.94); 
        --border-main: #1f883d; --border-neon: #00ff66; --border-cyber: #ff007f; --text-white: #fff; --border-sub: #161b22;
    }
    body { font-family: 'Courier New', Courier, monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 15px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; overflow-x: hidden; position: relative; }
    
    body::before { content: ''; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 255, 0, 0.02)); background-size: 100% 4px, 6px 100%; z-index: 2; pointer-events: none; }
    .cyber-grid-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(rgba(31, 136, 61, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(31, 136, 61, 0.04) 1px, transparent 1px); background-size: 20px 20px; z-index: 1; pointer-events: none; }
    .cyber-matrix-rain { position: fixed; top: -100px; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, transparent, rgba(0, 255, 102, 0.12) 50%, transparent); z-index: 1; pointer-events: none; animation: matrixRainFall 10s linear infinite; opacity: 0.3; }
    @keyframes matrixRainFall { 0% { transform: translateY(0); } 100% { transform: translateY(120vh); } }

    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1200px; margin: 0 auto 15px auto; border-bottom: 2px solid var(--border-main); padding-bottom: 12px; box-sizing: border-box; position: relative; z-index: 1000; }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 10px var(--border-neon), 0 0 20px var(--border-cyber); text-decoration: none; font-family: monospace; letter-spacing: 2px; }
    .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 6px; font-family: inherit; box-shadow: 0 0 10px rgba(0,255,102,0.15); }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; position: relative; z-index: 10; }
    
    /* 🛠️ هندسة لوحة الأركيد المخصصة وصندوق اللعبة الحصين */
    .game-master-wrapper { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 12px; padding: 20px; box-shadow: 0 25px 55px rgba(0,0,0,0.8), inset 0 0 20px rgba(0,255,102,0.05); border-bottom: 4px solid var(--border-neon); border-right: 4px solid var(--border-cyber); display: flex; flex-direction: column; align-items: center; gap: 15px; position: relative; z-index: 50; clip-path: polygon(0 0, 97% 0, 100% 3%, 100% 100%, 3% 100%, 0 97%); }
    .scoreboard-strip { display: flex; justify-content: space-between; width: 100%; max-width: 400px; font-size: 14px; font-weight: bold; color: var(--text-white); font-family: monospace; text-shadow: 0 0 5px var(--border-neon); border-bottom: 1px dashed var(--border-main); padding-bottom: 8px; }
    
    #snakeCanvas { background: #001100; border: 2px solid var(--border-main); box-shadow: 0 0 20px rgba(0,255,102,0.2), inset 0 0 15px rgba(0,255,102,0.1); border-radius: 6px; display: block; max-width: 100%; height: auto; }
    
    /* 📱 أزرار عصا التحكم اللمسية (Touch D-Pad) للهواتف الذكية */
    .dpad-container { display: none; grid-template-columns: repeat(3, 60px); grid-template-rows: repeat(3, 60px); gap: 8px; margin-top: 10px; justify-content: center; z-index: 100; }
    .dpad-btn { background: #0b1219; border: 2px solid var(--border-main); color: var(--border-neon); border-radius: 50%; font-size: 20px; display: flex; align-items: center; justify-content: center; cursor: pointer; user-select: none; -webkit-user-select: none; box-shadow: 0 0 8px rgba(0,255,102,0.1); }
    .dpad-btn:active { background: var(--border-neon); color: #000; box-shadow: 0 0 15px var(--border-neon); }
    
    @media (max-width: 850px) {
        .dpad-container { display: grid; }
        .responsive-profile-wrapper { padding: 15px; }
    }
</style>
"""
HOME_TERMINAL_CSS_PART2 = """
<style>
    /* 🕹️ حقن وتثبيت عمارة الستارة الجانبية المنبثقة دائرياً الموحدة لمنع التضارب والـ 404 كلياً */
    .sidebar-overlay { 
        position: fixed !important; top: 0 !important; right: 0 !important; 
        width: 320px !important; height: 100vh !important; 
        background: rgba(4, 6, 9, 0.98) !important; border-left: 2px solid var(--border-cyber) !important; 
        box-shadow: -25px 0 50px #000 !important; z-index: 99999999 !important; 
        display: flex !important; flex-direction: column !important; 
        padding: 30px 25px !important; box-sizing: border-box !important; 
        text-align: right !important; direction: rtl !important;
        clip-path: circle(0% at 100% 0%); transition: clip-path 0.45s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .sidebar-overlay.active { clip-path: circle(150% at 100% 0%) !important; }
    
    .close-menu-btn { background: #000; border: 1px solid var(--border-cyber); color: var(--border-cyber); font-size: 13px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: 4px; align-self: flex-start; margin-bottom: 25px; font-family: inherit; box-shadow: 0 0 10px rgba(255,0,127,0.15); }
    .close-menu-btn:hover { background: var(--border-cyber); color: #fff; box-shadow: 0 0 15px var(--border-cyber); }
    
    .sidebar-links-wrapper { display: flex; flex-direction: column; text-align: right; gap: 4px; }
    .section-menu-divider { font-size: 14px; font-weight: bold; display: flex; align-items: center; gap: 8px; justify-content: flex-start; margin-top: 15px; margin-bottom: 8px; border-bottom: 1px dashed var(--border-main); padding-bottom: 6px; color: #8b949e; letter-spacing: 0.5px; }
    
    .dropdown-trigger-btn { background: none; border: none; font-size: 15.5px; font-weight: bold; width: 100%; padding: 10px 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; color: var(--border-neon); text-shadow: 0 0 6px rgba(0,255,102,0.2); }
    .dropdown-content-panel { display: none; background: #000; border: 1px solid var(--border-main); border-radius: 4px; padding: 4px 12px; margin-bottom: 10px; flex-direction: column; }
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 9px 0; display: block; width: 100%; text-align: right; font-weight: 500; border-bottom: 1px dashed #161b22; }
    .game-link-btn:last-child { border-bottom: none; }
    
    .general-link-item { text-decoration: none; font-size: 15.5px; font-weight: bold; padding: 11px 0; display: block; font-family: inherit; color: var(--text-main); }
    .general-link-item:hover { color: var(--text-white); text-shadow: 0 0 10px var(--border-neon); padding-right: 4px; }
    .global-footer-bar { width: 100%; text-align: center; padding: 15px 0; border-top: 1px solid var(--border-main); font-size: 11.5px; color: var(--text-main); font-family: monospace; position: relative; z-index: 100; margin-top: auto; }
</style>
"""
def get_embedded_games_html():
    games_list_nodes = []
    try:
        games_dir = os.path.join(current_app.root_path, 'static', 'my_games')
        if os.path.exists(games_dir):
            for filename in sorted(os.listdir(games_dir)):
                if filename.endswith('.txt'):
                    game_slug = filename.replace('.txt', '').replace('\\n', '').replace('\\r', '').strip()
                    file_path = os.path.join(games_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        raw_lines = f.readlines()
                    lines = [str(line).replace('\\n', '').replace('\\r', '').strip() for line in raw_lines if line.strip()]
                    if len(lines) >= 3:
                        game_name = lines[0]
                        game_icon = lines[1]
                        game_color = lines[2]
                        node_html = f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>'
                        games_list_nodes.append(node_html)
    except Exception: pass
    return "".join(games_list_nodes) if games_list_nodes else '<p style="color:#1f883d; font-size:12px;">قائمة الألعاب فارغة.</p>'

@snake_blueprint.route('/snake')
def snake_page():
    dynamic_games_html = get_embedded_games_html()
    
    SNAKE_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CYBER_SNAKE_TERMINAL_v2026</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + SNAKE_TERMINAL_CSS + HOME_TERMINAL_CSS_PART2 + """
</head>
<body>
    <div class="cyber-grid-overlay"></div>
    <div class="cyber-matrix-rain"></div>

    <div class="top-nav">
        <a href="/" class="brand-logo">> ALBRAWE_</a>
        <button class="menu-btn-trigger" onclick="toggleSidebarMenu(true)"><i class="fas fa-terminal"></i> CORE_MENU_</button>
    </div>

    <div class="sidebar-overlay" id="slidingSidebarMenu">
        <button class="close-menu-btn" onclick="toggleSidebarMenu(false)"><i class="fas fa-times"></i> CLOSE_STREAM_</button>
        <div class="sidebar-links-wrapper">
            <a href="/" class="general-link-item">> البوابة الرئيسية 🏠</a>
            <button class="dropdown-trigger-btn" id="gamesMenuTrigger" onclick="toggleGamesDropdown()">
                <span>> قائمة ألعاب النظام 🎮</span><i class="fas fa-chevron-down arrow-icon"></i>
            </button>
            <div class="dropdown-content-panel" id="gamesDropdownPanel">""" + dynamic_games_html + """</div>
            <div class="section-menu-divider">SYS_ROUTING_UNITS</div>
            <a href="/projects" class="general-link-item">> معرض المشاريع 📁</a>
            <a href="/about" class="general-link-item">> الهوية الرقمية 👤</a>
            <a href="/scripts" class="general-link-item">> إسكربتات بايثون 💻</a>
            <a href="/report" class="general-link-item" style="color:var(--border-cyber);">> الإبلاغ عن مشكلة (صيانة) 🛠️</a>
            <a href="https://t.me" target="_blank" class="general-link-item" style="color:#388bfd;">> حسابي في التليجرام ✈️</a>
        </div>
    </div>

    <div class="main-container">
        <div class="game-master-wrapper">
            <div class="scoreboard-strip">
                <div>SCORE: <span id="scoreVal">000</span></div>
                <div>HIGH_SCORE: <span id="highScoreVal">000</span></div>
            </div>
            <canvas id="snakeCanvas" width="400" height="400"></canvas>
            
            <!-- لوحة التحكم اللمسية للموبايل -->
            <div class="dpad-container">
                <div></div><div class="dpad-btn" onclick="setDirection('UP')"><i class="fas fa-chevron-up"></i></div><div></div>
                <div class="dpad-btn" onclick="setDirection('LEFT')"><i class="fas fa-chevron-left"></i></div><div></div><div class="dpad-btn" onclick="setDirection('RIGHT')"><i class="fas fa-chevron-right"></i></div>
                <div></div><div class="dpad-btn" onclick="setDirection('DOWN')"><i class="fas fa-chevron-down"></i></div><div></div>
            </div>
        </div>
    </div>
    <div class="global-footer-bar">حقوق النشر محفوظة سيبرانياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©</div>
"""
    <script>
        // 🔊 محرك المزامنة السينثسيزر الصوتي المدمج لتوليد مؤثرات الـ 8-Bit دون ملفات خارجية
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playBleepSound(freq, duration, type="square") {
            try {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = type; osc.frequency.value = freq;
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + duration);
            } catch(e){}
        }

        const canvas = document.getElementById("snakeCanvas");
        const ctx = canvas.getContext("2d");
        const box = 20; let score = 0;
        let snake = [{x: 10 * box, y: 10 * box}, {x: 9 * box, y: 10 * box}];
        let food = { x: Math.floor(Math.random() * 19 + 1) * box, y: Math.floor(Math.random() * 19 + 1) * box };
        let d = "RIGHT"; let particles = [];

        // نظام جلب ومزامنة الـ High Score التراكمي من الذاكرة المحلية
        let localHighScore = localStorage.getItem("cyber_snake_highscore") || 0;
        document.getElementById("highScoreVal").innerText = String(localHighScore).padStart(3, '0');

        document.addEventListener("keydown", (e) => {
            if(e.keyCode == 37 && d != "RIGHT") d = "LEFT";
            else if(e.keyCode == 38 && d != "DOWN") d = "UP";
            else if(e.keyCode == 39 && d != "LEFT") d = "RIGHT";
            else if(e.keyCode == 40 && d != "UP") d = "DOWN";
        });

        function setDirection(dir) {
            if(dir == "LEFT" && d != "RIGHT") d = "LEFT";
            if(dir == "UP" && d != "DOWN") d = "UP";
            if(dir == "RIGHT" && d != "LEFT") d = "RIGHT";
            if(dir == "DOWN" && d != "UP") d = "DOWN";
        }

        // 💥 خوارزمية جزيئات الشظايا النيونية عند الأكل
        function spawnExplosion(x, y, color) {
            for(let i=0; i<12; i++) {
                particles.push({
                    x: x + box/2, y: y + box/2,
                    vx: (Math.random() - 0.5) * 5, vy: (Math.random() - 0.5) * 5,
                    alpha: 1, color: color
                });
            }
        }

        function draw() {
            ctx.fillStyle = "#001100"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // رسم وجر الثعبان التكتيكي مع توهج الحواف حياً
            for(let i=0; i<snake.length; i++) {
                ctx.fillStyle = (i == 0) ? "#00ff66" : "#125225";
                ctx.shadowBlur = (i == 0) ? 10 : 0; ctx.shadowColor = "#00ff66";
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
                ctx.shadowBlur = 0;
            }
            
            // رسم الهدية المشعة الفلورسنتية
            ctx.fillStyle = "#ff007f"; ctx.shadowBlur = 8; ctx.shadowColor = "#ff007f";
            ctx.fillRect(food.x, food.y, box, box); ctx.shadowBlur = 0;
            
            // رندر وتحديث الجزيئات المتفجرة
            particles.forEach((p, index) => {
                p.x += p.vx; p.y += p.vy; p.alpha -= 0.04;
                if(p.alpha <= 0) particles.splice(index, 1);
                else {
                    ctx.fillStyle = p.color; ctx.globalAlpha = p.alpha;
                    ctx.fillRect(p.x, p.y, 4, 4); ctx.globalAlpha = 1.0;
                }
            });

            let snakeX = snake[0].x; let snakeY = snake[0].y;
            if(d == "LEFT") snakeX -= box; if(d == "UP") snakeY -= box;
            if(d == "RIGHT") snakeX += box; if(d == "DOWN") snakeY += box;
            
            if(snakeX == food.x && snakeY == food.y) {
                score++; document.getElementById("scoreVal").innerText = String(score).padStart(3, '0');
                playBleepSound(523.25, 0.1, "sine"); // صوت الإمساك 8-Bit
                spawnExplosion(food.x, food.y, "#ff007f");
                food = { x: Math.floor(Math.random() * 19 + 1) * box, y: Math.floor(Math.random() * 19 + 1) * box };
            } else { snake.pop(); }
            
            let newHead = { x: snakeX, y: snakeY };
            if(snakeX < 0 || snakeX > canvas.width - box || snakeY < 0 || snakeY > canvas.height - box || collision(newHead, snake)) {
                playBleepSound(120, 0.4, "sawtooth"); // صوت الانفجار عند الخسارة
                alert("📡 CRYPTO_COLLISION: تحطم النواة! النقاط: " + score);
                if(score > localHighScore) { localStorage.setItem("cyber_snake_highscore", score); localHighScore = score; document.getElementById("highScoreVal").innerText = String(score).padStart(3, '0'); }
                snake = [{x: 10 * box, y: 10 * box}, {x: 9 * box, y: 10 * box}]; d = "RIGHT"; score = 0; document.getElementById("scoreVal").innerText = "000";
            }
            snake.unshift(newHead);
        }
        function collision(head, array) { for(let i=0; i<array.length; i++) { if(head.x == array[i].x && head.y == array[i].y) return true; } return false; }
        let game = setInterval(draw, 110);

        // 📊 عداد الربط التزامني لبث مدد الاستخدام حياً إلى رادار الأدمن والـ API
        setInterval(() => {
            const userName = localStorage.getItem('cyber_assigned_username') || "لاعب مجهول";
            fetch('/api/update_duration', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ username: userName, game: 'snake', durationIncrement: 4 })
            });
        }, 4000);

        function toggleSidebarMenu(openState) { const sidebar = document.getElementById("slidingSidebarMenu"); if(sidebar) { if(openState) sidebar.classList.add("active"); else sidebar.classList.remove("active"); } }
        function toggleGamesDropdown() { const panel = document.getElementById("gamesDropdownPanel"); panel.style.display = (panel.style.display === "flex") ? "none" : "flex"; }
    </script>
</body>
</html>
"""
    return render_template_string(SNAKE_HTML)
