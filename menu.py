import os
from flask import Blueprint, render_template_string, current_app, jsonify

menu_blueprint = Blueprint('menu', __name__)

# عزل التنسيقات الرقمية المتجاوبة تماماً للستارة ومفتاح تبديل الأنماط الحركي لعام 2026
MENU_CSS = """
<style>
    .sidebar-overlay { position: fixed; top: 0; right: -320px; width: 300px; height: 100vh; background: var(--bg-sidebar, rgba(10, 14, 20, 0.99)); border-left: 2px solid #58a6ff; box-shadow: -15px 0 35px rgba(0, 0, 0, 0.8); z-index: 99999; display: flex; flex-direction: column; padding: 25px 20px; box-sizing: border-box; transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1); overflow-y: auto; text-align: right; }
    .sidebar-overlay.active { right: 0 !important; }
    
    .close-menu-btn { background: none; border: none; color: #f85149; font-size: 14px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 5px; align-self: flex-end; margin-bottom: 25px; font-family: inherit; }
    .close-menu-btn:hover { text-shadow: 0 0 8px #f85149; }
    
    .sidebar-links-wrapper { display: flex; flex-direction: column; text-align: right; padding-right: 5px; }
    .section-menu-divider { font-size: 15px; font-weight: bold; display: flex; align-items: center; gap: 8px; justify-content: flex-start; margin-top: 15px; margin-bottom: 12px; border-bottom: 1px dashed var(--border-color, #21262d); padding-bottom: 6px; color: var(--text-muted, #8b949e); }
    
    .dropdown-trigger-btn { background: var(--bg-btn, #161b22); border: 1px solid var(--border-color, #30363d); color: #3fb950; font-size: 14.5px; font-weight: bold; width: 100%; padding: 12px; border-radius: 8px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; margin-bottom: 10px; transition: 0.2s; box-shadow: 0 4px 12px rgba(63,185,80,0.06); }
    .dropdown-trigger-btn:hover { border-color: #3fb950; box-shadow: 0 0 12px rgba(63,185,80,0.2); }
    .dropdown-trigger-btn i.arrow-icon { transition: transform 0.3s ease; font-size: 12px; }
    .dropdown-trigger-btn.open-state i.arrow-icon { transform: rotate(180deg); }
    
    .dropdown-content-panel { display: none; background: var(--bg-dropdown, #090d12); border: 1px solid var(--border-color, #21262d); border-radius: 8px; padding: 4px 12px; margin-bottom: 15px; flex-direction: column; }
    
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 10px 0; display: block; transition: 0.15s ease; width: 100%; text-align: right; font-weight: 500; border-bottom: 1px dashed var(--border-dashed, #161b22); }
    .game-link-btn:last-child { border-bottom: none; }
    .game-link-btn:hover { padding-right: 6px; text-shadow: 0 0 10px currentColor; }
    
    .general-link-item { text-decoration: none; font-size: 14px; color: var(--text-general, #c9d1d9); padding: 10px 0; display: block; font-weight: bold; transition: 0.2s; border-bottom: 1px solid var(--border-dashed, #161b22); }
    .general-link-item:hover { color: #58a6ff; text-shadow: 0 0 8px #58a6ff; padding-right: 4px; }
    
    /* 🌓 هندسة وتنسيق مفتاح الوضع الفاتح والداكن الأسفل المحمي */
    .theme-toggle-container { margin-top: auto; padding-top: 20px; border-top: 1px solid var(--border-color, #21262d); display: flex; justify-content: center; }
    .theme-toggle-btn { background: var(--bg-btn, #161b22); border: 1px solid var(--border-color, #30363d); color: var(--text-theme-btn, #58a6ff); font-size: 12.5px; font-weight: bold; width: 100%; padding: 10px; border-radius: 6px; cursor: pointer; font-family: inherit; display: flex; align-items: center; justify-content: center; gap: 8px; transition: 0.2s; }
    .theme-toggle-btn:hover { border-color: #58a6ff; box-shadow: 0 0 10px rgba(88,166,255,0.15); }
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
                        
                    game_name = lines[0] if len(lines) > 0 else game_slug
                    game_icon = lines[1] if len(lines) > 1 else "fas fa-gamepad"
                    game_color = lines[2] if len(lines) > 2 else "#fff"
                    
                    node_html = f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>'
                    games_list_nodes.append(node_html)
    except Exception:
        games_list_nodes = ['<p style="color:#8b949e; font-size:12px; padding:8px 0;">خطأ في مواءمة مسارات الألعاب.</p>']

    dynamic_games_html = "".join(games_list_nodes) if games_list_nodes else '<p style="color:#8b949e; font-size:12px; padding:8px 0;">لا توجد ألعاب مكتشفة حالياً.</p>'

    MENU_CANVAS_BODY = """
    <div class="sidebar-overlay" id="slidingSidebarMenu">
        <button class="close-menu-btn" onclick="toggleSidebarMenu(false)"><i class="fas fa-times"></i> إغلاق القائمة</button>
        <div class="sidebar-links-wrapper">
            <a href="/" class="general-link-item" style="color:var(--text-home-btn, #fff);">البوابة الرئيسية 🏠</a>
            
            <button class="dropdown-trigger-btn" id="gamesMenuTrigger" onclick="toggleGamesDropdown()">
                <span><i class="fas fa-gamepad" style="margin-left:5px;"></i> قائمة ألعاب النظام</span>
                <i class="fas fa-chevron-down arrow-icon"></i>
            </button>
            <div class="dropdown-content-panel" id="gamesDropdownPanel">
                """ + dynamic_games_html + """
            </div>
            
            <div class="section-menu-divider"><i class="fas fa-folder-open"></i> مسارات إضافية</div>
            <a href="/projects" class="general-link-item">معرض المشاريع 📁</a>
            <a href="/scripts" class="general-link-item">إسكربتات بايثون 💻</a>
            <a href="/report" class="general-link-item" style="color:#ff7b72;">الإبلاغ عن مشكلة (صيانة) 🛠️</a>
            <a href="https://t.me" target="_blank" class="general-link-item" style="color:#388bfd; border-bottom:none;">حسابي في التليجرام ✈️</a>
        </div>
        
        <!-- مفتاح تبديل الأنماط التفاعلي المستقر أسفل الستارة -->
        <div class="theme-toggle-container">
            <button class="theme-toggle-btn" onclick="toggleGlobalThemeMode()">
                <i class="fas fa-adjust"></i> <span id="themeToggleTextBtn">الوضع الفاتح ⚪</span>
            </button>
        </div>
    </div>
    """
    return jsonify({"html": MENU_CANVAS_BODY, "css": MENU_CSS})
