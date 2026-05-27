import os
from flask import Blueprint, render_template_string, current_app, jsonify

menu_blueprint = Blueprint('menu', __name__)

# 🎨 عزل الأنماط الفلورسنتية الحركية: هندسة الانبثاق الدائري من الزاوية، والنبض المتدرج للأزرار
MENU_CSS = """
<style>
    /* 🪐 هندسة الانبثاق الدائري المتمدد للستارة الجانبية من زاوية اليمين */
    .sidebar-overlay { 
        position: fixed !important; top: 0 !important; right: 0 !important; 
        width: 320px !important; height: 100vh !important; 
        background: rgba(8, 12, 20, 0.99) !important; 
        border-left: 2px solid #58a6ff !important; 
        box-shadow: -20px 0 40px rgba(0, 0, 0, 0.9) !important; 
        z-index: 9999999 !important; 
        display: flex !important; flex-direction: column !important; 
        padding: 30px 25px !important; box-sizing: border-box !important; 
        text-align: right !important;
        
        /* تأثير الدائرة التكتيكية التي تتمدد وتتضخم بروعة سينمائية */
        clip-path: circle(0% at 100% 0%);
        transition: clip-path 0.45s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .sidebar-overlay.active { 
        clip-path: circle(150% at 100% 0%) !important; 
    }
    
    /* زر الإغلاق النيوني التفاعلي X */
    .close-menu-btn { background: #161b22; border: 1px solid #30363d; color: #ff5555; font-size: 13.5px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: 6px; align-self: flex-start; margin-bottom: 30px; font-family: inherit; transition: 0.2s; }
    .close-menu-btn:hover { background: #ff5555; color: #fff; box-shadow: 0 0 12px #ff5555; }
    
    .sidebar-links-wrapper { display: flex; flex-direction: column; text-align: right; gap: 5px; }
    .section-menu-divider { font-size: 14.5px; font-weight: bold; display: flex; align-items: center; gap: 8px; justify-content: flex-start; margin-top: 15px; margin-bottom: 8px; border-bottom: 1px dashed #21262d; padding-bottom: 6px; color: #8b949e; }
    
    /* 📦 زر المنسدل التفاعلي الفاخر لباقة ألعاب النظام */
    .dropdown-trigger-btn { background: none; border: none; font-size: 15.5px; font-weight: bold; width: 100%; padding: 10px 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; margin: 4px 0; transition: 0.2s; animation: pulseArcadeGame 3s infinite alternate; }
    .dropdown-trigger-btn i.arrow-icon { transition: transform 0.3s ease; font-size: 12px; margin-right: auto; padding-left: 5px; }
    .dropdown-trigger-btn.open-state i.arrow-icon { transform: rotate(180deg); }
    
    .dropdown-content-panel { display: none; background: #05070b; border: 1px solid #21262d; border-radius: 8px; padding: 4px 12px; margin-bottom: 10px; flex-direction: column; }
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 9px 0; display: block; transition: 0.15s ease; width: 100%; text-align: right; font-weight: 500; border-bottom: 1px dashed #161b22; }
    .game-link-btn:last-child { border-bottom: none; }
    .game-link-btn:hover { padding-right: 6px; text-shadow: 0 0 10px currentColor; }
    
    /* ✨ شفرة النبض التكتيكي المتدرج للأزرار كنبضات القلب السيبرانية (Gradient Neon Pulse) */
    .general-link-item { text-decoration: none; font-size: 15.5px; font-weight: bold; padding: 11px 0; display: block; font-family: inherit; transition: transform 0.2s; }
    .general-link-item:hover { transform: translateX(-4px); }
    
    .link-home { color: #8b949e; animation: pulseHome 4s infinite alternate; }
    .link-projects { color: #a371f7; animation: pulseProjects 3.5s infinite alternate; }
    .link-about { color: #ff7b72; animation: pulseAbout 3.8s infinite alternate; }
    .link-scripts { color: #58a6ff; animation: pulseScripts 3.2s infinite alternate; }
    .link-report { color: #ff5555; animation: pulseReport 2.8s infinite alternate; }
    .link-telegram { color: #388bfd; border-bottom: none; animation: pulseTelegram 4.2s infinite alternate; }
    
    /* 💓 محرك أنميشن نبضات القلب اللوني المضيء الفلورسنتي بالملي حياً */
    @keyframes pulseHome { 0% { text-shadow: 0 0 4px rgba(255,255,255,0.2); color: #8b949e; } 100% { text-shadow: 0 0 14px #ffffff; color: #ffffff; } }
    @keyframes pulseArcadeGame { 0% { text-shadow: 0 0 4px rgba(63,185,80,0.2); color: #3fb950; } 100% { text-shadow: 0 0 15px #3fb950, 0 0 25px #ff007f; color: #ff007f; } }
    @keyframes pulseProjects { 0% { text-shadow: 0 0 4px rgba(163,113,247,0.2); color: #a371f7; } 100% { text-shadow: 0 0 14px #a371f7, 0 0 22px #00f0f0; color: #00f0f0; } }
    @keyframes pulseAbout { 0% { text-shadow: 0 0 4px rgba(255,123,114,0.2); color: #ff7b72; } 100% { text-shadow: 0 0 14px #ff7b72; color: #ff5555; } }
    @keyframes pulseScripts { 0% { text-shadow: 0 0 4px rgba(88,166,255,0.2); color: #58a6ff; } 100% { text-shadow: 0 0 14px #58a6ff, 0 0 20px #3fb950; color: #3fb950; } }
    @keyframes pulseReport { 0% { text-shadow: 0 0 4px rgba(255,85,85,0.2); color: #ff5555; } 100% { text-shadow: 0 0 16px #ff0000; color: #fff; } }
    @keyframes pulseTelegram { 0% { text-shadow: 0 0 4px rgba(56,139,253,0.2); color: #388bfd; } 100% { text-shadow: 0 0 14px #388bfd; color: #58a6ff; } }
</style>
"""
@menu_blueprint.route('/api/get_sidebar_menu')
def get_sidebar_menu():
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
                        lines = [line.replace('\\n', '').replace('\\r', '').strip() for line in raw_lines if line.strip()]
                        
                    game_name = lines if len(lines) > 0 else game_slug
                    game_icon = lines if len(lines) > 1 else "fas fa-gamepad"
                    game_color = lines if len(lines) > 2 else "#fff"
                    
                    node_html = f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>'
                    games_list_nodes.append(node_html)
    except Exception:
        games_list_nodes = ['<p style="color:#8b949e; font-size:12px; padding:8px 0;">خطأ في جلب مسارات باقة ألعاب النظام.</p>']

    dynamic_games_html = "".join(games_list_nodes) if games_list_nodes else '<p style="color:#8b949e; font-size:12px; padding:8px 0;">لا توجد ألعاب مستكشفة حالياً.</p>'

    MENU_CANVAS_BODY = """
    <div class="sidebar-overlay" id="slidingSidebarMenu">
        <button class="close-menu-btn" onclick="toggleSidebarMenu(false)"><i class="fas fa-times"></i> إغلاق القائمة</button>
        
        <div class="sidebar-links-wrapper">
            <a href="/" class="general-link-item link-home">البوابة الرئيسية</a>
            
            <button class="dropdown-trigger-btn" id="gamesMenuTrigger" onclick="toggleGamesDropdown()">
                <span>قائمة ألعاب النظام 🎮</span>
                <i class="fas fa-chevron-down arrow-icon"></i>
            </button>
            <div class="dropdown-content-panel" id="gamesDropdownPanel">
                """ + dynamic_games_html + """
            </div>
            
            <div class="section-menu-divider"><i class="fas fa-folder-open"></i> مسارات إضافية</div>
            <a href="/projects" class="general-link-item link-projects">معرض المشاريع 📁</a>
            <a href="/about" class="general-link-item link-about">الهوية الشخصية (About us) 👤</a>
            <a href="/scripts" class="general-link-item link-scripts">إسكربتات بايثون 💻</a>
            <a href="/report" class="general-link-item link-report" style="color:#ff7b72;">الإبلاغ عن مشكلة (صيانة) 🛠️</a>
            <a href="https://t.me" target="_blank" class="general-link-item link-telegram">حسابي في التليجرام ✈️</a>
        </div>
    </div>
    """
    return jsonify({"html": MENU_CANVAS_BODY, "css": MENU_CSS})
