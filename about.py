from flask import Blueprint, render_template_string, current_app

about_blueprint = Blueprint('about', __name__)

# عزل التنسيقات السيبرانية لحماية الأقواس من التعارض السحابي في خوادم فيرسيل
ABOUT_TERMINAL_CSS = """
<style>
    :root { --bg-global: #020406; --text-main: #3fb950; --bg-card: rgba(6, 10, 15, 0.92); --border-main: #1f883d; --border-neon: #58a6ff; --border-cyber: #3fb950; --text-white: #fff; --border-sub: #161b22; }
    body { font-family: 'Courier New', monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 0; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; overflow-x: hidden; position: relative; }
    body::before { content: ''; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 255, 0, 0.03)); background-size: 100% 4px, 6px 100%; z-index: 2; pointer-events: none; }
    .cyber-grid-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(rgba(31, 136, 61, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(31, 136, 61, 0.05) 1px, transparent 1px); background-size: 20px 20px; z-index: 1; pointer-events: none; }
    
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1200px; margin: 0 auto; padding: 15px 25px; box-sizing: border-box; position: relative; z-index: 1000; border-bottom: 1px solid var(--border-main); }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 10px var(--border-neon); text-decoration: none; font-family: monospace; letter-spacing: 2px; }
    .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; font-family: inherit; }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; max-width: 800px; margin: 0 auto; position: relative; z-index: 10; padding: 0 20px; box-sizing: border-box; }
    .about-box { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 12px; padding: 35px; width: 100%; max-width: 600px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); border-bottom: 4px solid var(--border-neon); border-left: 4px solid var(--border-cyber); box-sizing: border-box; text-align: right; direction: rtl; clip-path: polygon(0 0, 96% 0, 100% 5%, 100% 100%, 4% 100%, 0 95%); }
    
    .highlight-title { font-size: 18px; color: var(--text-white); margin-top: 0; margin-bottom: 15px; border-bottom: 1px dashed var(--border-main); padding-bottom: 8px; text-shadow: 0 0 5px rgba(255,255,255,0.2); }
    .about-text { font-size: 14px; line-height: 1.7; color: var(--text-main); margin-bottom: 20px; }
    .global-footer-bar { width: 100%; text-align: center; padding: 20px 0; border-top: 1px solid var(--border-main); font-size: 11.5px; color: var(--text-main); font-family: monospace; position: relative; z-index: 100; margin-top: auto; letter-spacing: 1px; }

    /* 🕹 * حقن وتثبيت معايير الستارة الجانبية المدمجة لمنع تكرار الحقن والتداخل البصري */
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
    @media (max-width: 850px) { body { padding: 15px; } .top-nav { max-width: 100%; } .about-box { clip-path: none !important; } }
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
                        game_name = lines
                        game_icon = lines
                        game_color = lines
                        node_html = f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>'
                        games_list_nodes.append(node_html)
    except Exception: pass
    return "".join(games_list_nodes) if games_list_nodes else '<p style="color:#1f883d; font-size:12px;">قائمة الألعاب فارغة.</p>'

@about_blueprint.route('/about')
def about_page():
    dynamic_games_html = get_embedded_games_html()

    ABOUT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>About Us | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + ABOUT_TERMINAL_CSS + """
</head>
<body>
    <div class="cyber-grid-overlay"></div>
    <div class="top-nav">
        <a href="/" class="brand-logo">> ALBRAWE_</a>
        <button class="menu-btn-trigger" onclick="toggleSidebarMenu(true)"><i class="fas fa-terminal"></i> CORE_MENU_</button>
    </div>

    <!-- الستارة الجانبية مدمجة ومصبوبة حياً داخل نفس ملف صفحة التعريف لمنع التداخل والـ 404 كلياً للابد حياً -->
    <div class="sidebar-overlay" id="slidingSidebarMenu">
        <button class="close-menu-btn" onclick="toggleSidebarMenu(false)"><i class="fas fa-times"></i> CLOSE_STREAM_</button>
        <div class="sidebar-links-wrapper">
            <a href="/" class="general-link-item link-home">> البوابة الرئيسية 🏠</a>
            <button class="dropdown-trigger-btn" onclick="toggleGamesDropdown()">
                <span>> قائمة ألعاب النظام 🎮</span>
                <i class="fas fa-chevron-down arrow-icon"></i>
            </button>
            <div class="dropdown-content-panel" id="gamesDropdownPanel">
                """ + dynamic_games_html + """
            </div>
            <div class="section-menu-divider">SYS_ROUTING_UNITS</div>
            <a href="/projects" class="general-link-item link-projects">> معرض المشاريع 📁</a>
            <a href="/about" class="general-link-item link-about">> الهوية الرقمية 👤</a>
            <a href="/scripts" class="general-link-item link-scripts">> إسكربتات بايثون 💻</a>
            <a href="/report" class="general-link-item link-report">> الإبلاغ عن مشكلة (صيانة) 🛠️</a>
            <a href="https://t.me" target="_blank" class="general-link-item" style="color:#388bfd;">> حسابي في التليجرام ✈️</a>
        </div>
    </div>

    <div class="main-container">
        <div class="about-box">
            <h3 class="highlight-title"><i class="fas fa-user-shield" style="color:var(--border-neon); margin-left:6px;"></i> الهوية الرقمية للمنصة لعام 2026</h3>
            <p class="about-text">
                تم تأسيس وتطوير هذا الخادم السحابي المحصن كمنظومة متكاملة تجمع بين الفن المعماري القياسي وهندسة البرمجيات المتقدمة لتقديم بيئة أركيد نيونية متجاوبة حياً، مع تزويدها برادار رصد بياني فوري فائق الدقة.
            </p>
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
    return render_template_string(ABOUT_HTML)
