from flask import Blueprint, render_template_string, current_app

report_blueprint = Blueprint('report', __name__)

# عزل التنسيقات السيبرانية لحماية بايثون من التعارض النصي للأقواس خارج الصندوق في خوادم فيرسيل
REPORT_TERMINAL_CSS = """
<style>
    :root { 
        --bg-global: #030508; --text-main: #c9d1d9; --bg-card: rgba(13, 17, 23, 0.9); 
        --border-main: #21262d; --border-neon: #ff5555; --border-cyber: #ff007f; --text-white: #fff; --border-sub: #30363d; 
    }
    body { font-family: 'Courier New', monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 0; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; position: relative; overflow-x: hidden; }
    
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 800px; margin: 0 auto; padding: 15px 25px; box-sizing: border-box; position: relative; z-index: 1000; border-bottom: 1px solid var(--border-sub); }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 10px var(--border-neon); text-decoration: none; font-family: monospace; letter-spacing: 2px; }
    .menu-btn-trigger { background: #161b22; border: 1px solid var(--border-sub); color: var(--border-neon); padding: 8px 18px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; font-family: inherit; }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; max-width: 800px; margin: 0 auto; position: relative; z-index: 10; padding: 0 20px; box-sizing: border-box; }
    
    /* 🛠️ هندسة واجهة شاشة الإدخال والاختراق السيبراني العسكري (Command Line Breach) */
    .form-box { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 14px; padding: 30px; width: 100%; max-width: 500px; box-shadow: 0 20px 50px rgba(255,0,0,0.1); border-bottom: 4px solid var(--border-neon); border-left: 4px solid var(--border-cyber); box-sizing: border-box; text-align: right; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }
    .form-group { margin-bottom: 18px; display: flex; flex-direction: column; gap: 6px; }
    label { font-weight: bold; color: var(--text-white); font-size: 13.5px; font-family: monospace; letter-spacing: 0.5px; }
    
    input, textarea { padding: 12px; background: #04060a; border: 1px solid var(--border-main); border-radius: 6px; color: #ff5555; font-family: monospace; width: 100%; box-sizing: border-box; font-size: 13px; text-shadow: 0 0 5px rgba(255,85,85,0.5); box-shadow: inset 0 0 10px rgba(0,0,0,0.8); }
    input:focus, textarea:focus { border-color: var(--border-cyber); outline: none; box-shadow: 0 0 10px rgba(255,0,127,0.2); }
    
    .submit-btn { background: var(--border-neon); color: #fff; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; font-family: inherit; margin-top: 10px; font-size: 14px; transition: 0.2s; text-transform: uppercase; letter-spacing: 0.5px; }
    .submit-btn:hover { box-shadow: 0 0 15px var(--border-neon); background: var(--border-cyber); }
    .global-footer-bar { width: 100%; text-align: center; padding: 20px 0; border-top: 1px solid var(--border-sub); font-size: 12px; color: #8b949e; font-family: monospace; position: relative; z-index: 100; margin-top: auto; }

    /* 🕹️ حقن وتثبيت معايير الستارة الجانبية المنبثقة دائرياً الموحدة لمنع التضارب والـ 404 */
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
    .dropdown-trigger-btn { background: none; border: none; font-size: 15.5px; font-weight: bold; width: 100%; padding: 10px 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; color: #3fb950; text-shadow: 0 0 4px rgba(63,185,80,0.2); }
    .dropdown-content-panel { display: none; background: #000; border: 1px solid var(--border-main); border-radius: 4px; padding: 4px 12px; margin-bottom: 10px; flex-direction: column; }
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 9px 0; display: block; width: 100%; text-align: right; font-weight: 500; border-bottom: 1px dashed #161b22; }
    .game-link-btn:last-child { border-bottom: none; }
    .general-link-item { text-decoration: none; font-size: 15.5px; font-weight: bold; padding: 11px 0; display: block; font-family: inherit; color: #3fb950; }
    .link-home { color: #8b949e; } .link-projects { color: #a371f7; } .link-about { color: #ff7b72; } .link-scripts { color: #58a6ff; } .link-report { color: #ff5555; }
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
                    
                    # ✅ التطهير البرمجي وقفل الفهارس صراحة لمنع الـ 500 والتحميل المعلق نهائياً حياً
                    lines = [str(line).replace('\\n', '').replace('\\r', '').strip() for line in raw_lines if line.strip()]
                    if len(lines) >= 3:
                        game_name = lines[0]
                        game_icon = lines[1]
                        game_color = lines[2]
                        node_html = f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>'
                        games_list_nodes.append(node_html)
    except Exception: pass
    return "".join(games_list_nodes) if games_list_nodes else '<p style="color:#1f883d; font-size:12px;">قائمة الألعاب فارغة.</p>'

@report_blueprint.route('/report')
def report_page():
    dynamic_games_html = get_embedded_games_html()

    REPORT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>البلاغات والصيانة | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + REPORT_TERMINAL_CSS + """
</head>
<body>
    <div class="top-nav">
        <a href="/" class="brand-logo">> ALBRAWE_</a>
        <button class="menu-btn-trigger" onclick="toggleSidebarMenu(true)"><i class="fas fa-terminal"></i> CORE_MENU_</button>
    </div>

    <!-- الستارة الجانبية منبثقة دائرياً ومدمجة في نفس الملف لمنع تداخل الكروت نهائياً للابد حياً -->
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
            <a href="https://t.me" target="_blank" class="general-link-item style="color:#388bfd;">> حسابي في التليجرام ✈️</a>
        </div>
    </div>

    <div class="main-container">
        <div class="form-box">
            <h3 style="margin-top:0; color:var(--text-white); border-bottom:1px solid var(--border-sub); padding-bottom:8px; font-family:monospace;"><i class="fas fa-terminal" style="color:var(--border-cyber); margin-left:5px;"></i> SYSTEM_BREACH_REPORT_LOG v1.0</h3>
            <div class="form-group">
                <label>> DEFINE_REPORTER_IDENTITY_NAME:</label>
                <input type="text" id="reporterName" placeholder="[اكتب معرف الاسم الفريد هنا...]" autocomplete="off">
            </div>
            <div class="form-group">
                <label>> ENCODE_ERROR_DESCRIPTION_DETAILS:</label>
                <textarea id="complaintDetails" rows="4" placeholder="[اكتب شرح العطل البرمي بالتفصيل هنا...]"></textarea>
            </div>
            <button class="submit-btn" onclick="sendComplaintPayload()">EXECUTE_PAYLOAD_SUBMIT 🚀</button>
        </div>
    </div>
    <div class="global-footer-bar">حقوق النشر محفوظة سيبرانياً وتعود إلى المسؤول البراوي بتاريخ 2026 © [STABLE_BUILD]</div>

    <script>
        function sendComplaintPayload() {
            const user = document.getElementById("reporterName").value.trim();
            const details = document.getElementById("complaintDetails").value.trim();
            if(!user || !details) { alert("❌ CRITICAL_ERROR: الحقول فارغة!"); return; }
            fetch('/api/submit_complaint', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ user: user, details: details })
            }).then(res => {
                if(res.ok) { alert("🟢 INJECTION_SUCCESSFUL: تم استلام البلاغ وحقن الهوية بنجاح."); document.getElementById("reporterName").value=""; document.getElementById("complaintDetails").value=""; }
            }).catch(() => { alert("❌ CONNECTION_FAILED."); });
        }
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
    return render_template_string(REPORT_HTML)
