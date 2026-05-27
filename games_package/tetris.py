from flask import Blueprint, render_template_string

tetris_blueprint = Blueprint('tetris', __name__)

TETRIS_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>لعبة Tetris | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --bg-global: #06090d; --text-main: #c9d1d9; --bg-card: #0d1117; --border-main: #30363d; --border-neon: #d29922; --text-white: #fff; --border-sub: #21262d; }
        [data-theme="light"] { --bg-global: #f6f8fa; --text-main: #24292f; --bg-card: #ffffff; --border-main: #d0d7de; --border-neon: #bf8700; --text-white: #1f2328; --border-sub: #d0d7de; }
        body { font-family: 'Courier New', monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 25px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; align-items: center; transition: 0.3s; }
        
        .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 500px; margin-bottom: 25px; border-bottom: 2px solid var(--border-sub); padding-bottom: 12px; }
        .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 8px var(--border-neon); text-decoration: none; font-family: monospace; }
        .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; font-family: inherit; }
        
        .game-box { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 14px; padding: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.4); border-bottom: 4px solid var(--border-neon); display: flex; flex-direction: column; align-items: center; gap: 15px; width: 100%; max-width: 360px; box-sizing: border-box; }
        canvas { background: #04060a; border: 2px solid var(--border-main); border-radius: 8px; display: block; max-width: 100%; }
        .score-board { font-size: 18px; font-weight: bold; color: var(--text-white); font-family: monospace; }
        
        .controls-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 180px; margin-top: 5px; }
        .control-btn { background: #161b22; border: 1px solid #30363d; color: #fff; padding: 12px; border-radius: 8px; font-size: 16px; cursor: pointer; text-align: center; }
        .control-btn:active { background: var(--border-neon); color: #000; }
        
        @media (min-width: 850px) { .controls-grid { display: none; } }
        .global-footer-bar { width: 100%; max-width: 500px; text-align: center; margin-top: 30px; padding-top: 15px; border-top: 1px solid var(--border-sub); font-size: 12px; color: var(--text-main); font-family: monospace; }
    </style>
    <script>
        (function() { const savedTheme = localStorage.getItem("albrawe_global_theme_mode") || "dark"; document.documentElement.setAttribute("data-theme", savedTheme); })();
    </script>
</head>
<body>
    <div class="top-nav">
        <a href="/" class="brand-logo">Albrawe</a>
        <button class="menu-btn-trigger" onclick="loadAndOpenSidebarMenu()"><i class="fas fa-bars"></i> القائمة</button>
    </div>
    <div id="dynamicMenuInjectionZone"></div>

    <div class="game-box">
        <div class="score-board">النقاط: <span id="tetrisScore">0</span></div>
        <canvas id="tetrisCanvas" width="240" height="400"></canvas>
        
        <div class="controls-grid">
            <div></div><button class="control-btn" onclick="movePiece(0, -1)"><i class="fas fa-rotate"></i></button><div></div>
            <button class="control-btn" onclick="movePiece(-1, 0)"><i class="fas fa-chevron-left"></i></button>
            <button class="control-btn" onclick="dropPiece()"><i class="fas fa-arrow-down"></i></button>
            <button class="control-btn" onclick="movePiece(1, 0)"><i class="fas fa-chevron-right"></i></button>
        </div>
    </div>

    <div class="global-footer-bar">حقوق النشر محفوظة برمجياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©</div>

    <script>
        const canvas = document.getElementById("tetrisCanvas");
        const ctx = canvas.getContext("2d");
        const ROW = 20; const COL = 12; const SQ = 20;
        let score = 0;

        function drawSquare(x, y, color) {
            ctx.fillStyle = color; ctx.fillRect(x*SQ, y*SQ, SQ, SQ);
            ctx.strokeStyle = "#06090d"; ctx.strokeRect(x*SQ, y*SQ, SQ, SQ);
        }

        let board = [];
        for(let r=0; r<ROW; r++) { board[r] = []; for(let c=0; c<COL; c++) { board[r][c] = "#04060a"; } }

        function drawBoard() { for(let r=0; r<ROW; r++) { for(let c=0; c<COL; c++) { drawSquare(c, r, board[r][c]); } } }
        drawBoard();

        const PIECES = [
            [[[1,1,1,1]], "cyan"],
            [[[1,1,1],[0,1,0]], "purple"],
            [[[1,1,0],[0,1,1]], "red"],
            [[[0,1,1],[1,1,0]], "green"],
            [[[1,1],[1,1]], "yellow"]
        ];

        let activePiece = getRandomPiece();

        function getRandomPiece() {
            let r = Math.floor(Math.random() * PIECES.length);
            return { matrix: PIECES[r][0], color: PIECES[r][1], x: 4, y: 0 };
        }

        function drawPiece() {
            activePiece.matrix.forEach((row, rIdx) => {
                row.forEach((val, cIdx) => {
                    if(val) drawSquare(activePiece.x + cIdx, activePiece.y + rIdx, activePiece.color);
                });
            });
        }

        function clearPiece() {
            activePiece.matrix.forEach((row, rIdx) => {
                row.forEach((val, cIdx) => {
                    if(val) drawSquare(activePiece.x + cIdx, activePiece.y + rIdx, "#04060a");
                });
            });
        }

        function movePiece(dx, dy) {
            clearPiece();
            activePiece.x += dx;
            if (dy === -1) {
                // تدوير مصفوفة المكعبات الحركية
                let nMatrix = activePiece.matrix[0].map((val, index) => activePiece.matrix.map(row => row[index]).reverse());
                activePiece.matrix = nMatrix;
            } else { activePiece.y += dy; }
            if(collision()) { activePiece.x -= dx; if(dy === -1) { } else { activePiece.y -= dy; lockPiece(); } }
            drawPiece();
        }

        function collision() {
            for(let r=0; r<activePiece.matrix.length; r++) {
                for(let c=0; c<activePiece.matrix[r].length; c++) {
                    if(!activePiece.matrix[r][c]) continue;
                    let newX = activePiece.x + c; let newY = activePiece.y + r;
                    if(newX < 0 || newX >= COL || newY >= ROW) return true;
                    if(newY < 0) continue;
                    if(board[newY][newX] !== "#04060a") return true;
                }
            }
            return false;
        }

        function lockPiece() {
            for(let r=0; r<activePiece.matrix.length; r++) {
                for(let c=0; c<activePiece.matrix[r].length; c++) {
                    if(!activePiece.matrix[r][c]) continue;
                    if(activePiece.y + r < 0) { alert("🚨 إنتهت اللعبة الكتلية!"); resetBoard(); return; }
                    board[activePiece.y + r][activePiece.x + c] = activePiece.color;
                }
            }
            for(let r=0; r<ROW; r++) {
                if(board[r].every(val => val !== "#04060a")) {
                    board.splice(r, 1); board.unshift(new Array(COL).fill("#04060a"));
                    score += 10; document.getElementById("tetrisScore").innerText = score;
                }
            }
            drawBoard(); activePiece = getRandomPiece();
        }

        function dropPiece() { movePiece(0, 1); }
        setInterval(dropPiece, 1000);

        function resetBoard() {
            score = 0; document.getElementById("tetrisScore").innerText = score;
            board = []; for(let r=0; r<ROW; r++) { board[r] = []; for(let c=0; c<COL; c++) { board[r][c] = "#04060a"; } }
            drawBoard(); activePiece = getRandomPiece();
        }

        document.addEventListener("keydown", e => {
            if(e.keyCode === 37) movePiece(-1, 0);
            else if(e.keyCode === 38) movePiece(0, -1);
            else if(e.keyCode === 39) movePiece(1, 0);
            else if(e.keyCode === 40) movePiece(0, 1);
        });

        function loadAndOpenSidebarMenu() {
            const zone = document.getElementById("dynamicMenuInjectionZone");
            if (zone.innerHTML.trim() !== "") { toggleSidebarMenu(true); return; }
            fetch('/api/get_sidebar_menu').then(res => res.json()).then(data => {
                const styleNode = document.createElement("style"); styleNode.innerHTML = data.css; document.head.appendChild(styleNode);
                zone.innerHTML = data.html; setTimeout(() => { toggleSidebarMenu(true); }, 30);
            });
        }
        function toggleSidebarMenu(openState) { const sidebar = document.getElementById("slidingSidebarMenu"); if(sidebar) { if(openState) sidebar.classList.add("active"); else sidebar.classList.remove("active"); } }
        function toggleGamesDropdown() { const trigger = document.getElementById("gamesMenuTrigger"); const panel = document.getElementById("gamesDropdownPanel"); if(panel.style.display === "flex") { panel.style.display = "none"; trigger.classList.remove("open-state"); } else { panel.style.display = "flex"; trigger.classList.add("open-state"); } }
    </script>
</body>
</html>
"""

@tetris_blueprint.route('/tetris')
def tetris_page():
    return render_template_string(TETRIS_HTML)
