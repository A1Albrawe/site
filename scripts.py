import os
from flask import Blueprint, render_template_string, current_app

scripts_blueprint = Blueprint('scripts', __name__)

# عزل التنسيقات الفلورسنتية العائمة لحماية الأقواس من التعارض السحابي في خوادم فيرسيل
SCRIPTS_CSS = """
<style>
    :root { --bg-global: #030508; --text-main: #c9d1d9; --bg-card: rgba(13, 17, 23, 0.85); --border-main: #21262d; --border-neon: #58a6ff; --border-cyber: #3fb950; --text-white: #fff; --border-sub: #30363d; }
    body { font-family: 'Courier New', monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 0; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; overflow-x: hidden; position: relative; }
    
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1200px; margin: 0 auto; padding: 15px 25px; box-sizing: border-box; position: relative; z-index: 1000; border-bottom: 1px solid var(--border-sub); }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 10px var(--border-neon); text-decoration: none; font-family: monospace; }
    .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; font-family: inherit; }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 1000px; margin: 30px auto; gap: 20px; position: relative; z-index: 10; padding: 0 20px; box-sizing: border-box; }
    
    /* 🛸 هندسة "الكرت الدوار الذكي العائم" (Floating & Rotating Cyber Code Cards) */
    .code-box-card { 
        background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 12px; padding: 25px; width: 100%; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.5); border-top: 4px solid var(--border-neon); border-left: 4px solid var(--border-cyber); 
        text-align: right; box-sizing: border-box; margin-bottom: 15px; backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
        animation: cyberFloat 4s ease-in-out infinite alternate; transition: transform 0.3s, box-shadow 0.3s;
    }
    .code-box-card:hover { transform: translateY(-6px) scale(1.01); border-color: var(--border-cyber); box-shadow: 0 0 20px rgba(63,185,80,0.15); }
    @keyframes cyberFloat { 0% { transform: translateY(0px); } 100% { transform: translateY(-8px); } }
    
    pre { background: #04060a; padding: 15px; border-radius: 6px; border: 1px solid var(--border-sub); color: #3fb950; font-family: monospace; font-size: 13px; overflow-x: auto; direction: ltr; text-align: left; margin: 10px 0 0 0; box-shadow: inset 0 0 10px rgba(0,0,0,0.8); }
    .global-footer-bar { width: 100%; text-align: center; padding: 20px 0; border-top: 1px solid var(--border-sub); font-size: 12px; color: #8b949e; font-family: monospace; position: relative; z-index: 100; margin-top: auto; }

    /* 🕹️ حقن وتثبيت معايير الستارة الجانبية المدمجة لمنع تكرار الحقن والتداخل البصري */
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
    .dropdown-trigger-btn { background: none; border: none; font-size: 15.5px; font-weight: bold; width: 100%; padding: 10px 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; color: #3fb950; text-shadow: 0 0 4px rgba(63,185,80,0.2); }
    .dropdown-content-panel { display: none; background: #05070b; border: 1px solid #21262d; border-radius: 8px; padding: 4px 12px; margin-bottom: 10px; flex-direction: column; }
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 9px 0; display: block; width: 100%; text-align: right; font-weight: 500; border-bottom: 1px dashed #161b22; }
    .game-link-btn:last-child { border-bottom: none; }
    .general-link-item { text-decoration: none; font-size: 15.5px; font-weight: bold; padding: 11px 0; display: block; font-family: inherit; }
    .link-home { color: #8b949e; animation: pulseHome 4s infinite alternate; } .link-projects { color: #a371f7; } .link-about { color: #ff7b72; } .link-scripts { color: #58a6ff; } .link-report { color: #ff5555; }
    @keyframes pulseHome { 0% { text-shadow: 0 0 4px rgba(255,255,255,0.2); color: #8b949e; } 100% { text-shadow: 0 0 14px #ffffff; color: #ffffff; } }
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

@scripts_blueprint.route('/scripts')
def scripts_page():
    dynamic_games_html = get_embedded_games_html()
    dynamic_scripts_html = ""
    try:
        scr_dir = os.path.join(current_app.root_path, 'static', 'my_scripts')
        if os.path.exists(scr_dir):
            for filename in sorted(os.listdir(scr_dir)):
                if filename.endswith('.txt'):
                    file_path = os.path.join(scr_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        raw_lines = f.readlines()
                    
                    # ✅ التطهير البرمجي والتحويل النصي الصريح للمصفوفة لمنع الـ AttributeError والـ 500 نهائياً
                    lines = [str(line).replace('\\n', '').replace('\\r', '').strip() for line in raw_lines if line.strip()]
                    
                    if len(lines) >= 2:
                        s_title = lines
                        s_desc = lines
                        s_code = "\\n".join(lines[2:])
                        
                        dynamic_scripts_html += f'''
                        <div class="code-box-card">
                            <h3 style="margin-top:0; color:var(--text-white); font-size:16px;"><i class="fas fa-code" style="color:var(--border-cyber); margin-left:6px;"></i> {s_title}</h3>
                            <p style="font-size:13px; margin:0 0 10px 0;">{s_desc}</p>
                            <pre><code>{s_code}</code></pre>
                        </div>
                        '''
    except Exception: pass

    if not dynamic_scripts_html:
        dynamic_scripts_html = '<p style="color:#8b949e; text-align:center; width:100%;">مستودع السكريبتات فارغ حالياً.</p>'

    SCRIPTS_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>مستودع السكريبتات | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + SCRIPTS_CSS + """
</head>
<body>
    <div class="top-nav">
        <a href="/" class="brand-logo">Albrawe</a>
        <button class="menu-btn-trigger" onclick="toggleSidebarMenu(true)"><i class="fas fa-bars"></i> القائمة</button>
    </div>

    <!-- الستارة الجانبية مدمجة ومصبوبة حياً داخل نفس ملف السكريبتات لمنع التعليق والـ 404 كلياً -->
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
        """ + dynamic_scripts_html + """
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
    return render_template_string(SCRIPTS_HTML)
