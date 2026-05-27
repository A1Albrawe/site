import os
from flask import Blueprint, render_template_string, current_app

projects_blueprint = Blueprint('projects', __name__)

PROJECTS_CSS = """
<style>
    :root {
        --bg-global: #06090d; --text-main: #c9d1d9; --bg-card: #0d1117; 
        --border-main: #30363d; --border-neon: #a371f7; --border-cyber: #00f0f0; --text-white: #fff; --border-sub: #21262d;
    }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 0; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; overflow-x: hidden; }
    
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1200px; margin: 0 auto; padding: 15px 25px; box-sizing: border-box; position: relative; z-index: 1000; border-bottom: 1px solid var(--border-sub); }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 8px var(--border-neon); text-decoration: none; font-family: monospace; }
    .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 6px; font-family: inherit; }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 1200px; margin: 30px auto; padding: 0 25px; box-sizing: border-box; position: relative; z-index: 10; }
    .proj-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; width: 100%; text-align: right; direction: rtl; }
    
    /* 🛸 هندسة "الكرت الدوار الذكي العائم" المتجاوب للمشاريع */
    .proj-card { 
        background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 14px; padding: 25px; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.5); border-top: 4px solid var(--border-neon); border-left: 4px solid var(--border-cyber); 
        display: flex; flex-direction: column; gap: 12px; animation: cyberFloat 4s ease-in-out infinite alternate;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .proj-card:hover { transform: translateY(-6px) scale(1.01); border-color: var(--border-cyber); box-shadow: 0 0 20px rgba(0,240,240,0.15); }
    @keyframes cyberFloat { 0% { transform: translateY(0px); } 100% { transform: translateY(-8px); } }
    
    .proj-title { font-size: 17px; font-weight: bold; color: var(--text-white); margin: 0; }
    .proj-desc { font-size: 13.5px; color: var(--text-main); line-height: 1.6; margin: 0; }
    .global-footer-bar { width: 100%; text-align: center; padding: 20px 0; border-top: 1px solid var(--border-sub); font-size: 12px; color: #8b949e; font-family: monospace; margin-top: auto; }

    /* 🕹️ حقن وتثبيت تصميم ومقاييس الستارة الجانبية المنبثقة دائرياً الموحدة في نفس الملف */
    .sidebar-overlay { 
        position: fixed !important; top: 0 !important; right: 0 !important; 
        width: 320px !important; height: 100vh !important; 
        background: rgba(8, 12, 20, 0.99) !important; border-left: 2px solid #58a6ff !important; 
        box-shadow: -20px 0 40px rgba(0, 0, 0, 0.9) !important; z-index: 99999999 !important; 
        display: flex !important; flex-direction: column !important; 
        padding: 30px 25px !important; box-sizing: border-box !important; 
        text-align: right !important; direction: rtl !important;
        clip-path: circle(0% at 100% 0%); transition: clip-path 0.45s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .sidebar-overlay.active { clip-path: circle(150% at 100% 0%) !important; }
    .close-menu-btn { background: #161b22; border: 1px solid #30363d; color: #ff5555; font-size: 13.5px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: 6px; align-self: flex-start; margin-bottom: 25px; font-family: inherit; }
    .sidebar-links-wrapper { display: flex; flex-direction: column; text-align: right; gap: 5px; }
    .section-menu-divider { font-size: 14.5px; font-weight: bold; display: flex; align-items: center; gap: 8px; justify-content: flex-start; margin-top: 15px; margin-bottom: 8px; border-bottom: 1px dashed #21262d; padding-bottom: 6px; color: #8b949e; }
    .dropdown-trigger-btn { background: none; border: none; font-size: 15.5px; font-weight: bold; width: 100%; padding: 10px 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; animation: pulseArcadeGame 3s infinite alternate; }
    .dropdown-content-panel { display: none; background: #05070b; border: 1px solid #21262d; border-radius: 8px; padding: 4px 12px; margin-bottom: 10px; flex-direction: column; }
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 9px 0; display: block; width: 100%; text-align: right; font-weight: 500; border-bottom: 1px dashed #161b22; }
    .game-link-btn:last-child { border-bottom: none; }
    .general-link-item { text-decoration: none; font-size: 15.5px; font-weight: bold; padding: 11px 0; display: block; font-family: inherit; }
    .link-home { color: #8b949e; animation: pulseHome 4s infinite alternate; }
    .link-projects { color: #a371f7; animation: pulseProjects 3.5s infinite alternate; }
    .link-about { color: #ff7b72; animation: pulseAbout 3.8s infinite alternate; }
    .link-scripts { color: #58a6ff; animation: pulseScripts 3.2s infinite alternate; }
    .link-report { color: #ff5555; animation: pulseReport 2.8s infinite alternate; }
    .link-telegram { color: #388bfd; }
    
    @keyframes pulseHome { 0% { text-shadow: 0 0 4px rgba(255,255,255,0.2); color: #8b949e; } 100% { text-shadow: 0 0 14px #ffffff; color: #ffffff; } }
    @keyframes pulseArcadeGame { 0% { text-shadow: 0 0 4px rgba(63,185,80,0.2); color: #3fb950; } 100% { text-shadow: 0 0 15px #3fb950, 0 0 25px #ff007f; color: #ff007f; } }
    @keyframes pulseProjects { 0% { text-shadow: 0 0 4px rgba(163,113,247,0.2); color: #a371f7; } 100% { text-shadow: 0 0 14px #a371f7, 0 0 22px #00f0f0; color: #00f0f0; } }
    @keyframes pulseAbout { 0% { text-shadow: 0 0 4px rgba(255,123,114,0.2); color: #ff7b72; } 100% { text-shadow: 0 0 14px #ff7b72; color: #ff5555; } }
    @keyframes pulseScripts { 0% { text-shadow: 0 0 4px rgba(88,166,255,0.2); color: #58a6ff; } 100% { text-shadow: 0 0 14px #58a6ff, 0 0 20px #3fb950; color: #3fb950; } }
    @keyframes pulseReport { 0% { text-shadow: 0 0 4px rgba(255,85,85,0.2); color: #ff5555; } 100% { text-shadow: 0 0 16px #ff0000; color: #fff; } }
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
                    game_name = lines if len(lines) > 0 else game_slug
                    game_icon = lines if len(lines) > 1 else "fas fa-gamepad"
                    game_color = lines if len(lines) > 2 else "#fff"
                    node_html = f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>'
                    games_list_nodes.append(node_html)
    except Exception: pass
    return "".join(games_list_nodes) if games_list_nodes else '<p style="color:#8b949e; font-size:12px;">قائمة الألعاب فارغة.</p>'

@projects_blueprint.route('/projects')
def projects_page():
    dynamic_games_html = get_embedded_games_html()
    dynamic_projects_html = ""
    try:
        proj_dir = os.path.join(current_app.root_path, 'static', 'my_projects')
        if os.path.exists(proj_dir):
            for filename in sorted(os.listdir(proj_dir)):
                if filename.endswith('.txt'):
                    file_path = os.path.join(proj_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        raw_lines = f.readlines()
                    lines = [str(line).replace('\\n', '').replace('\\r', '').strip() for line in raw_lines if line.strip()]
                    if len(lines) >= 2:
                        p_title = lines
                        p_desc = lines
                        dynamic_projects_html += f'''
                        <div class="proj-card">
                            <div class="proj-title"><i class="fas fa-drafting-table" style="color:var(--border-cyber); margin-left:6px;"></i> {p_title}</div>
                            <p class="proj-desc">{p_desc}</p>
                        </div>
                        '''
    except Exception: pass

    if not dynamic_projects_html:
        dynamic_projects_html = '<p style="color:#8b949e; text-align:center; grid-column: 1/-1;">لا توجد مشاريع مرفوعة حالياً.</p>'

    PROJECTS_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>معرض المشاريع | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + PROJECTS_CSS + """
</head>
<body>
    <div class="top-nav">
        <a href="/" class="brand-logo">Albrawe</a>
        <button class="menu-btn-trigger" onclick="toggleSidebarMenu(true)"><i class="fas fa-bars"></i> القائمة</button>
    </div>

    <!-- الستارة الجانبية مدمجة ومصبوبة حياً داخل نفس ملف معرض المشاريع لمنع الـ 404 كلياً -->
    <div class="sidebar-overlay" id="slidingSidebarMenu">
        <button class="close-menu-btn" onclick="toggleSidebarMenu(false)"><i class="fas fa-times"></i> إغلاق القائمة</button>
        <div class="sidebar-links-wrapper">
            <a href="/" class="general-link-item link-home">البوابة الرئيسية</a>
            <button class="dropdown-trigger-btn" onclick="toggleGamesDropdown()">
                <span>قائمة ألعاب النظام 🎮</span>
                <i class="fas fa-chevron-down arrow-icon"></i>
            </button>
            <div class="dropdown-content-panel" id="gamesDropdownPanel">
                """ + dynamic_games_html + """
            </div>
            <div class="section-menu-divider">مسارات إضافية</div>
            <a href="/projects" class="general-link-item link-projects">معرض المشاريع 📁</a>
            <a href="/about" class="general-link-item link-about">(About us) 👤</a>
            <a href="/scripts" class="general-link-item link-scripts">إسكربتات بايثون 💻</a>
            <a href="/report" class="general-link-item link-report">الإبلاغ عن مشكلة (صيانة) 🛠️</a>
            <a href="https://t.me" target="_blank" class="general-link-item link-telegram">حسابي في التليجرام ✈️</a>
        </div>
    </div>

    <div class="main-container">
        <div class="proj-grid">
            """ + dynamic_projects_html + """
        </div>
    </div>
    <div class="global-footer-bar">حقوق النشر محفوظة برمجياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©</div>

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
    return render_template_string(PROJECTS_HTML)
