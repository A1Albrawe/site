import os
from flask import Blueprint, current_app, jsonify

menu_blueprint = Blueprint('menu', __name__)

# 🪐 عزل أنماط لوحة التحكم المظلمة: دمج خلفية الأسد القوطي وتوسيط الاسم المضيء بالملي
MENU_CSS = """
<style>
    /* 🕹️ علبة الستارة الجانبية الطولية الفخمة المثبتة صراحة بأقصى يمين الشاشة */
    .sidebar-overlay { 
        position: fixed !important; top: 0 !important; right: -340px !important; 
        width: 310px !important; height: 100vh !important; 
        background: #06090d !important; 
        border-left: 2px solid #58a6ff !important; 
        box-shadow: -20px 0 40px rgba(0, 0, 0, 0.9) !important; 
        z-index: 99999999 !important; 
        display: flex !important; flex-direction: column !important; 
        padding: 25px 20px !important; box-sizing: border-box !important; 
        text-align: right !important; direction: rtl !important;
        transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        overflow-y: auto !important;
    }
    .sidebar-overlay.active { right: 0 !important; }
    
    /* ❌ زر الإغلاق النيوني التفاعلي المحمي بأعلى طبقة منعاً للتعليق البصري */
    .close-menu-btn { background: rgba(22, 27, 34, 0.8); border: 1px solid #30363d; color: #ff5555; font-size: 13px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 6px; align-self: flex-start; margin-bottom: 20px; font-family: inherit; z-index: 100000000 !important; transition: 0.2s; }
    .close-menu-btn:hover { background: #ff5555; color: #fff; box-shadow: 0 0 10px #ff5555; }
    
    /* 🦁 صندوق الهوية القوطي الفاخر الحاوي لصورة الأسد وتوسيط الاسم المضيء أسفلها بالملي */
    .lion-identity-card { 
        width: 100%; height: 180px; 
        background: linear-gradient(to bottom, rgba(11,15,23,0.4) 0%, #0b0f17 100%), url('https://ibb.co') no-repeat center center;
        background-size: cover; border-radius: 12px; border: 1px solid #21262d;
        margin-bottom: 25px; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; padding-bottom: 15px; box-sizing: border-box; box-shadow: inset 0 0 20px #000, 0 10px 20px rgba(0,0,0,0.5);
    }
    /* الاسم المضيء الفخم المتموضع بدقة هندسية أسفل صورة الأسد */
    .lion-brand-title { font-size: 26px; font-weight: 900; color: #fff; font-family: 'Courier New', monospace; letter-spacing: 2px; text-transform: uppercase; margin: 0; text-shadow: 0 0 10px #58a6ff, 0 0 20px rgba(88,166,255,0.4); }
    
    .sidebar-links-wrapper { display: flex; flex-direction: column; text-align: right; gap: 4px; }
    .section-menu-divider { font-size: 14.5px; font-weight: bold; display: flex; align-items: center; gap: 8px; justify-content: flex-start; margin-top: 12px; margin-bottom: 6px; border-bottom: 1px dashed #21262d; padding-bottom: 4px; color: #8b949e; }
    
    /* 📦 هندسة زر المنسدل التفاعلي الفاخر لباقة ألعاب النظام المكتشفة تلقائياً */
    .dropdown-trigger-btn { background: none; border: none; font-size: 15.5px; font-weight: bold; width: 100%; padding: 10px 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; color: #3fb950; text-shadow: 0 0 4px rgba(63,185,80,0.2); }
    .dropdown-trigger-btn i.arrow-icon { transition: transform 0.3s ease; font-size: 12px; margin-right: auto; padding-left: 5px; }
    .dropdown-trigger-btn.open-state i.arrow-icon { transform: rotate(180deg); }
    
    .dropdown-content-panel { display: none; background: #05070b; border: 1px solid #21262d; border-radius: 8px; padding: 4px 12px; margin-bottom: 10px; flex-direction: column; }
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 9px 0; display: block; transition: 0.15s ease; width: 100%; text-align: right; font-weight: 500; border-bottom: 1px dashed #161b22; }
    .game-link-btn:last-child { border-bottom: none; }
    .game-link-btn:hover { padding-right: 6px; text-shadow: 0 0 10px currentColor; }
    
    /* روابط القائمة والخطوط الفلورسنتية النبضية الممتدة حياً */
    .general-link-item { text-decoration: none; font-size: 15.5px; font-weight: bold; padding: 11px 0; display: block; font-family: inherit; transition: 0.2s; }
    .link-home { color: #8b949e; } .link-home:hover { color: #fff; }
    .link-projects { color: #a371f7; } .link-projects:hover { text-shadow: 0 0 8px #a371f7; }
    .link-about { color: #ff7b72; } .link-about:hover { text-shadow: 0 0 8px #ff7b72; }
    .link-scripts { color: #58a6ff; } .link-scripts:hover { text-shadow: 0 0 8px #58a6ff; }
    .link-report { color: #ff5555; } .link-report:hover { text-shadow: 0 0 8px #ff5555; }
    .link-telegram { color: #388bfd; } .link-telegram:hover { text-shadow: 0 0 8px #388bfd; }
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
                    lines = [str(line).replace('\\n', '').replace('\\r', '').strip() for line in raw_lines if line.strip()]
                        
                    game_name = lines if len(lines) > 0 else game_slug
                    game_icon = lines if len(lines) > 1 else "fas fa-gamepad"
                    game_color = lines if len(lines) > 2 else "#fff"
                    
                    node_html = f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>'
                    games_list_nodes.append(node_html)
    except Exception:
        games_list_nodes = ['<p style="color:#8b949e; font-size:12px;">خطأ في جلب مسارات الألعاب التلقائية.</p>']

    dynamic_games_html = "".join(games_list_nodes) if games_list_nodes else '<p style="color:#8b949e; font-size:12px;">لا توجد ألعاب مكتشفة حالياً.</p>'

    MENU_CANVAS_BODY = """
    <div class="sidebar-overlay" id="slidingSidebarMenu">
        <button class="close-menu-btn" onclick="toggleSidebarMenu(false)"><i class="fas fa-times"></i> إغلاق القائمة</button>
        
        <!-- 🦁 حقن كرت الأسد المظلم الفاخر وتوسيط الاسم البرمي أسفله مباشرة -->
        
            <h2 class="lion-brand-title">albrawe</h2>
        </div>
        
        <div class="sidebar-links-wrapper">
            <!-- 1️⃣ البوابة الرئيسية -->
            <a href="/" class="general-link-item link-home">البوابة الرئيسية</a>
            
            <!-- 2️⃣ قائمة ألعاب النظام التلقائية المنسدلة بنعومة -->
            <button class="dropdown-trigger-btn" id="gamesMenuTrigger" onclick="toggleGamesDropdown()">
                <span>قائمة ألعاب النظام 🎮</span>
                <i class="fas fa-chevron-down arrow-icon"></i>
            </button>
            <div class="dropdown-content-panel" id="gamesDropdownPanel">
                """ + dynamic_games_html + """
            </div>
            
            <!-- الترتيب والمسارات الإضافية القياسية كاملة ودون نقصان -->
            <div class="section-menu-divider">مسارات إضافية</div>
            <a href="/projects" class="general-link-item link-projects">معرض المشاريع 📁</a>
            <a href="/about" class="general-link-item link-about">(About us) 👤</a>
            <a href="/scripts" class="general-link-item link-scripts">إسكربتات بايثون 💻</a>
            <a href="/report" class="general-link-item link-report">الإبلاغ عن مشكلة (صيانة) 🛠️</a>
            <a href="https://t.me" target="_blank" class="general-link-item link-telegram">حسابي في التليجرام ✈️</a>
        </div>
    </div>
    """
    return jsonify({"html": MENU_CANVAS_BODY, "css": MENU_CSS})
