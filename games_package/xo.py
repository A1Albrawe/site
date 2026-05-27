from flask import Blueprint, render_template_string

xo_blueprint = Blueprint('xo', __name__)

XO_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>لعبة X-O | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --bg-global: #06090d; --text-main: #c9d1d9; --bg-card: #0d1117; --border-main: #30363d; --border-neon: #a371f7; --text-white: #fff; --border-sub: #21262d; }
        [data-theme="light"] { --bg-global: #f6f8fa; --text-main: #24292f; --bg-card: #ffffff; --border-main: #d0d7de; --border-neon: #8250df; --text-white: #1f2328; --border-sub: #d0d7de; }
        body { font-family: 'Courier New', monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 25px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; align-items: center; transition: 0.3s; }
        .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 500px; margin-bottom: 25px; border-bottom: 2px solid var(--border-sub); padding-bottom: 12px; }
        .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 8px var(--border-neon); text-decoration: none; font-family: monospace; }
        .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; font-family: inherit; }
        .game-box { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 14px; padding: 25px; box-shadow: 0 20px 40px rgba(0,0,0,0.4); border-bottom: 4px solid var(--border-neon); display: flex; flex-direction: column; align-items: center; gap: 15px; width: 100%; max-width: 360px; box-sizing: border-box; }
        .xo-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%; aspect-ratio: 1; }
        .cell { background: #161b22; border: 1px solid var(--border-main); border-radius: 8px; font-size: 36px; font-weight: bold; color: var(--text-white); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.15s; font-family: monospace; }
        .cell:hover { background: rgba(163,113,247,0.05); border-color: var(--border-neon); }
        .status-txt { font-size: 16px; font-weight: bold; color: var(--text-white); margin-bottom: 5px; }
        .reset-btn { background: var(--bg-global); border: 1px solid var(--border-main); color: var(--text-white); padding: 8px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; font-family: inherit; font-size: 13px; transition: 0.2s; }
        .reset-btn:hover { border-color: var(--border-neon); }
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
        <div class="status-txt" id="gameStatus">الدور على اللاعب: X</div>
        <div class="xo-grid">
            <div class="cell" onclick="makeMove(this, 0)"></div>
            <div class="cell" onclick="makeMove(this, 1)"></div>
            <div class="cell" onclick="makeMove(this, 2)"></div>
            <div class="cell" onclick="makeMove(this, 3)"></div>
            <div class="cell" onclick="makeMove(this, 4)"></div>
            <div class="cell" onclick="makeMove(this, 5)"></div>
            <div class="cell" onclick="makeMove(this, 6)"></div>
            <div class="cell" onclick="makeMove(this, 7)"></div>
            <div class="cell" onclick="makeMove(this, 8)"></div>
        </div>
        <button class="reset-btn" onclick="resetMatrix()">إعادة اللعب <i class="fas fa-redo"></i></button>
    </div>

    <div class="global-footer-bar">حقوق النشر محفوظة برمجياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©</div>

    <script>
        let turn = "X"; let board = ["", "", "", "", "", "", "", "", ""]; let isGameOver = false;

        // ✅ إحياء وإغلاق مصفوفة الفوز الثمانية لإنهاء وتحطيم الـ Syntax Error كلياً
        const winPatterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ];

        function makeMove(cell, index) {
            if (board[index] !== "" || isGameOver) return;
            board[index] = turn; cell.innerText = turn;
            cell.style.color = turn === "X" ? "#58a6ff" : "#a371f7";
            cell.style.textShadow = turn === "X" ? "0 0 10px #58a6ff" : "0 0 10px #a371f7";

            checkWinner();
            if (!isGameOver) {
                turn = turn === "X" ? "O" : "X";
                document.getElementById("gameStatus").innerText = "الدور على اللاعب: " + turn;
            }
        }

        function checkWinner() {
            for (let pattern of winPatterns) {
                if (board[pattern[0]] && board[pattern[0]] === board[pattern[1]] && board[pattern[0]] === board[pattern[2]]) {
                    document.getElementById("gameStatus").innerText = "🎉 انتصر اللاعب: " + board[pattern[0]];
                    isGameOver = true; return;
                }
            }
            if (!board.includes("")) { document.getElementById("gameStatus").innerText = "🤝 تعادل صلب بين الطرفين!"; isGameOver = true; }
        }

        function resetMatrix() {
            turn = "X"; board = ["", "", "", "", "", "", "", "", ""]; isGameOver = false;
            document.getElementById("gameStatus").innerText = "الدور على اللاعب: X";
            document.querySelectorAll(".cell").forEach(c => { c.innerText = ""; c.style.textShadow = "none"; });
        }

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

@xo_blueprint.route('/xo')
def xo_page():
    return render_template_string(XO_HTML)
