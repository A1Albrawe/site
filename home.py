import os
from flask import Blueprint, render_template_string, current_app

home_blueprint = Blueprint('home', __name__)

# الأنماط السيبرانية الحركية الكاملة لـ مصفوفة شلالات الرموز والشبكة الرادارية العسكرية التكتيكية
HOME_TERMINAL_CSS = """
<style>
    :root {
        --bg-global: #020406; --text-main: #3fb950; --bg-card: rgba(6, 10, 15, 0.92); 
        --border-main: #1f883d; --border-neon: #00ff66; --border-cyber: #ff007f; --text-white: #fff; --border-sub: #161b22;
    }
    body { font-family: 'Courier New', Courier, monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 25px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; overflow-x: hidden; position: relative; }
    body::before { content: ''; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 255, 0, 0.03)); background-size: 100% 4px, 6px 100%; z-index: 2; pointer-events: none; }
    .cyber-grid-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(rgba(31, 136, 61, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(31, 136, 61, 0.05) 1px, transparent 1px); background-size: 20px 20px; z-index: 1; pointer-events: none; }
    .cyber-matrix-rain { position: fixed; top: -100px; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, transparent, rgba(0, 255, 102, 0.15) 50%, transparent); z-index: 1; pointer-events: none; animation: matrixRainFall 8s linear infinite; opacity: 0.4; }
    @keyframes matrixRainFall { 0% { transform: translateY(0); } 100% { transform: translateY(120vh); } }
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1200px; margin: 0 auto 30px auto; border-bottom: 2px solid var(--border-main); padding-bottom: 14px; box-sizing: border-box; position: relative; z-index: 1000; }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 10px var(--border-neon), 0 0 20px var(--border-cyber); text-decoration: none; font-family: monospace; letter-spacing: 2px; }
    .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 6px; font-family: inherit; box-shadow: 0 0 10px rgba(0,255,102,0.15); }
    .menu-btn-trigger:hover { background: var(--border-neon); color: #000; box-shadow: 0 0 20px var(--border-neon); }
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; position: relative; z-index: 10; }
    .responsive-profile-wrapper { display: flex; flex-direction: row; gap: 40px; width: 100%; max-width: 1200px; background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 12px; padding: 45px; box-shadow: 0 25px 55px rgba(0,0,0,0.8), inset 0 0 20px rgba(0,255,102,0.05); border-bottom: 4px solid var(--border-neon); border-right: 4px solid var(--border-cyber); box-sizing: border-box; align-items: center; direction: rtl; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); position: relative; z-index: 50; clip-path: polygon(0 0, 97% 0, 100% 4%, 100% 100%, 3% 100%, 0 96%); }
    .profile-sidebar-zone { flex: 1; max-width: 280px; display: flex; flex-direction: column; align-items: center; text-align: center; border-left: 2px solid var(--border-main); padding-left: 30px; box-sizing: border-box; }
    .profile-content-zone { flex: 2; display: flex; flex-direction: column; justify-content: center; text-align: right; box-sizing: border-box; padding-right: 15px; }
    .avatar-wrapper { width: 150px; height: 150px; border-radius: 8px; border: 2px solid var(--border-cyber); overflow: hidden; box-shadow: 0 0 25px rgba(255,0,127,0.3); margin-bottom: 20px; display: flex; align-items: center; justify-content: center; background: #000; position: relative; }
    .avatar-wrapper::before { content: ''; position: absolute; width: 100%; height: 100%; border: 2px dashed var(--border-neon); border-radius: 50%; animation: radarSpin 10s linear infinite; pointer-events: none; scale: 1.1; opacity: 0.6; }
    @keyframes radarSpin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .avatar-img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .profile-name { font-size: 32px; font-weight: bold; color: var(--text-white); margin: 0 0 6px 0; text-shadow: 0 0 10px rgba(255,255,255,0.4); letter-spacing: 1px; }
    .profile-title { font-size: 11px; font-weight: bold; color: var(--border-neon); margin: 0; text-transform: uppercase; letter-spacing: 1.5px; text-shadow: 0 0 8px var(--border-neon); }
    .details-sub-box { display: flex; flex-direction: column; gap: 18px; font-size: 14.5px; line-height: 1.7; }
    .meta-item { display: block; color: var(--text-main); text-shadow: 0 0 4px rgba(63,185,80,0.15); }
    .meta-label { font-weight: bold; color: var(--text-white); font-family: monospace; }
    .tech-highlight { color: #58a6ff; font-weight: bold; font-family: monospace; text-shadow: 0 0 8px rgba(88,166,255,0.4); }
    .global-footer-bar { width: 100%; text-align: center; padding: 20px 0; border-top: 1px solid var(--border-main); font-size: 11.5px; color: var(--text-main); font-family: monospace; position: relative; z-index: 100; margin-top: auto; letter-spacing: 1px; }
    .sidebar-overlay { position: fixed !important; top: 0 !important; right: 0 !important; width: 320px !important; height: 100vh !important; background: rgba(4, 6, 9, 0.98) !important; border-left: 2px solid var(--border-cyber) !important; box-shadow: -25px 0 50px #000 !important; z-index: 99999999 !important; display: flex !important; flex-direction: column !important; padding: 30px 25px !important; box-sizing: border-box !important; text-align: right !important; direction: rtl !important; clip-path: circle(0% at 100% 0%); transition: clip-path 0.45s cubic-bezier(0.4, 0, 0.2, 1) !important; }
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
    @media (max-width: 850px) { body { padding: 15px; } .top-nav { max-width: 100%; } .responsive-profile-wrapper { flex-direction: column; align-items: center; padding: 25px; max-width: 440px; clip-path: none !important; } .profile-sidebar-zone { flex: none; width: 100%; max-width: 100%; border-left: none; border-bottom: 2px solid var(--border-main); padding-left: 0; padding-bottom: 25px; margin-bottom: 20px; } .profile-content-zone { width: 100%; padding-right: 0; } }
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
                    
                    # ✅ تصحيح أمني صارم: قفل وسحق الأخطاء بجلب الفهارس المباشرة بدلاً من المصفوفة العارية
                    lines = [str(line).replace('\\n', '').replace('\\r', '').strip() for line in raw_lines if line.strip()]
                    if len(lines) >= 3:
                        game_name = lines[0]
                        game_icon = lines[1]
                        game_color = lines[2]
                        node_html = f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>'
                        games_list_nodes.append(node_html)
    except Exception: pass
    return "".join(games_list_nodes) if games_list_nodes else '<p style="color:#1f883d; font-size:12px;">قائمة الألعاب فارغة.</p>'

@home_blueprint.route('/')
def home_page():
    dynamic_games_html = get_embedded_games_html()
    
    HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ALBRAWE_TERMINAL_OS_v2026</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + HOME_TERMINAL_CSS + """
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
                <span>> قائمة ألعاب النظام 🎮</span>
                <i class="fas fa-chevron-down arrow-icon"></i>
            </button>
            <div class="dropdown-content-panel" id="gamesDropdownPanel">
                """ + dynamic_games_html + """
            </div>
            <div class="section-menu-divider">SYS_ROUTING_UNITS</div>
            <a href="/projects" class="general-link-item">> معرض المشاريع 📁</a>
            <a href="/about" class="general-link-item">> الهوية الرقمية 👤</a>
            <a href="/scripts" class="general-link-item">> إسكربتات بايثون 💻</a>
            <a href="/report" class="general-link-item" style="color:var(--border-cyber);">> الإبلاغ عن مشكلة (صيانة) 🛠️</a>
            <a href="https://t.me" target="_blank" class="general-link-item" style="color:#388bfd;">> حسابي في التليجرام ✈️</a>
        </div>
    </div>

    <div class="main-container">
        <div class="responsive-profile-wrapper">
            <div class="profile-sidebar-zone">
                <div class="avatar-wrapper">
                    <img class="avatar-img" src="/static/avatar.png" alt="Albrawe Profile" onerror="this.src='https://flagcdn.com'">
                </div>
                <h1 class="profile-name">Albrawe</h1>
                <div class="profile-title">> SECURE_CORE_ENGINEER</div>
            </div>
            <div class="profile-content-zone">
                <div class="details-sub-box">
                    <span class="meta-item">
                        ⚡ <span class="meta-label">[SYS_INFO]:</span> بناء وتطوير تطبيقات الويب الكاملة، وتصميم وتعديل اسكريبتات البايثون الحصينة. إنشاء وتصميم واجهات الويب المتكاملة، معالجة السجلات المحلية، وتوليد القنوات السيبرانية الذكية.
                    </span>
                    <span class="meta-item" style="border-top: 1px dashed var(--border-main); padding-top: 12px; margin-top: 2px;">
                        🛠️ <span class="meta-label">[CORE_STACK]:</span>
                        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                            <div>■ <span class="tech-highlight">Python (Flask_Runtime)</span></div>
                            <div>■ <span class="tech-highlight">JavaScript (Async_ES6)</span></div>
                        </div>
                    </span>
                </div>
            </div>
        </div>
    </div>
    <div class="global-footer-bar">حقوق النشر محفوظة سيبرانياً وتعود إلى المسؤول البراوي بتاريخ 2026 © [STABLE_BUILD]</div>

    <script>
        function toggleSidebarMenu(openState) {
            const sidebar = document.getElementById("slidingSidebarMenu");
            if (sidebar) {
                if(openState) sidebar.classList.add("active");
                else sidebar.classList.remove("active");
            }
        }
        function toggleGamesDropdown() {
            const panel = document.getElementById("gamesDropdownPanel");
            panel.style.display = (panel.style.display === "flex") ? "none" : "flex";
        }
    </script>
</body>
</html>
"""
    return render_template_string(HOME_HTML)
