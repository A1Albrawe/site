from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

# عزل التنسيقات الفلورسنتية الحركية لمحاكاة ملفك الشخصي بالملي وبدون تداخل الأقواس
HOME_CSS_PART1 = """
<style>
    :root {
        --bg-global: #06090d; --text-main: #c9d1d9; --bg-card: #0d1117; 
        --border-main: #30363d; --border-neon: #58a6ff; --border-cyber: #3fb950; --text-white: #fff; --border-sub: #21262d;
    }
    
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 0; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; overflow-x: hidden; }
    
    /* 🌐 شريط التوجيه القياسي العلوي الموحد لجميع الواجهات */
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1200px; margin: 0 auto; padding: 15px 25px; box-sizing: border-box; position: relative; z-index: 1000; border-bottom: 1px solid var(--border-sub); }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 8px var(--border-neon); text-decoration: none; font-family: monospace; cursor: pointer; }
    .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 6px; font-family: inherit; transition: 0.2s; }
    .menu-btn-trigger:hover { background: var(--border-neon); color: #000; box-shadow: 0 0 12px var(--border-neon); }
    
    .profile-master-container { width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 15px 40px 15px; box-sizing: border-box; position: relative; z-index: 10; }
    
    /* 🦁 هندسة غلاف الأسد القوطي المظلم والاسم البرمي المتوهج المستنسخ بالبكسل حياً */
    .cyber-profile-cover { width: 100%; height: 350px; border-radius: 0 0 18px 18px; border: 1px solid var(--border-main); border-bottom: 4px solid var(--border-neon); position: relative; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; padding-bottom: 30px; box-sizing: border-box; box-shadow: 0 15px 35px rgba(0,0,0,0.6); background-color: #0d1117; background-position: center center; background-repeat: no-repeat; background-size: cover; transition: background 0.3s ease; }
    .cover-brand-name { font-size: 55px; font-weight: 900; color: #fff; letter-spacing: 3px; font-family: 'Courier New', monospace; text-transform: uppercase; margin: 0; text-shadow: 0 0 12px #58a6ff, 0 0 25px rgba(88,166,255,0.5); position: relative; z-index: 5; }
</style>
"""
HOME_CSS_PART2 = """
<style>
    /* 🖼️ هندسة ومقاييس الأفاتار الدائري التداخلي المتطابق كلياً مع صورتك الموثقة حياً */
    .profile-meta-row { display: flex; align-items: flex-end; gap: 30px; margin-top: -65px; padding: 0 40px; box-sizing: border-box; width: 100%; direction: rtl; position: relative; z-index: 100; transform-style: preserve-3d; transform: perspective(1000px); }
    .avatar-wrapper-circle { width: 155px; height: 155px; border-radius: 50%; border: 5px solid var(--bg-global); overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5); background: #04060a; flex-shrink: 0; transition: transform 0.25s ease; display: flex; align-items: center; justify-content: center; }
    .avatar-img-circle { width: 100%; height: 100%; object-fit: cover; display: block; }
    
    .profile-identity-zone { flex: 1; text-align: right; padding-bottom: 15px; }
    .user-full-name { font-size: 28px; font-weight: bold; color: var(--text-white); margin: 0 0 5px 0; display: flex; align-items: center; gap: 10px; }
    .user-slug-name { font-size: 18px; color: #8b949e; font-family: monospace; font-weight: 500; }
    .followers-badge-line { font-size: 13.5px; color: #8b949e; margin: 8px 0 0 0; font-weight: 500; }
    .followers-count { color: var(--text-white); font-weight: bold; }
    
    /* 🛠️ أجنحة لوحة المعلومات الموثقة لجامعة عين شمس والثانوية */
    .info-dashboard-card { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 14px; padding: 30px; margin-top: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); text-align: right; direction: rtl; box-sizing: border-box; border-right: 4px solid var(--border-cyber); }
    .dashboard-title-row { display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: bold; color: #58a6ff; margin-bottom: 20px; border-bottom: 1px solid var(--border-sub); padding-bottom: 10px; }
    
    .meta-info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
    .info-item-box { display: flex; align-items: center; gap: 12px; font-size: 14.5px; color: var(--text-main); line-height: 1.5; }
    .info-item-box i { color: #8b949e; width: 20px; text-align: center; font-size: 16px; }
    .highlight-text-blue { color: #58a6ff; font-weight: bold; text-decoration: none; }
    .global-footer-bar { width: 100%; text-align: center; padding-top: 15px; border-top: 1px solid var(--border-sub); font-size: 12px; color: #8b949e; font-family: monospace; position: relative; z-index: 100; margin-top: auto; padding: 20px 0; }
</style>
"""
# 🪐 الجزء الثالث: الهندسة الجانبية الصارمة للستارة ومحرك النبض التكتيكي الملون للأزرار
HOME_CSS_PART3 = """
<style>
    .sidebar-overlay { 
        position: fixed !important; top: 0 !important; right: 0 !important; 
        width: 320px !important; height: 100vh !important; 
        background: rgba(8, 12, 20, 0.99) !important; 
        border-left: 2px solid #58a6ff !important; 
        box-shadow: -20px 0 40px rgba(0, 0, 0, 0.9) !important; 
        z-index: 99999999 !important; 
        display: flex !important; flex-direction: column !important; 
        padding: 30px 25px !important; box-sizing: border-box !important; 
        text-align: right !important; direction: rtl !important;
        
        /* 🕹️ تثبيت وتحقيق الانبثاق الدائري المتمدد من زاوية اليمين العلوية بالملي */
        clip-path: circle(0% at 100% 0%);
        transition: clip-path 0.45s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .sidebar-overlay.active { clip-path: circle(150% at 100% 0%) !important; }
    
    .close-menu-btn { background: #161b22; border: 1px solid #30363d; color: #ff5555; font-size: 13.5px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: 6px; align-self: flex-start; margin-bottom: 25px; font-family: inherit; z-index: 100000000 !important; }
    .close-menu-btn:hover { background: #ff5555; color: #fff; box-shadow: 0 0 12px #ff5555; }
    
    .sidebar-links-wrapper { display: flex; flex-direction: column; text-align: right; gap: 5px; }
    .section-menu-divider { font-size: 14.5px; font-weight: bold; display: flex; align-items: center; gap: 8px; justify-content: flex-start; margin-top: 15px; margin-bottom: 8px; border-bottom: 1px dashed #21262d; padding-bottom: 6px; color: #8b949e; }
    
    .dropdown-trigger-btn { background: none; border: none; font-size: 15.5px; font-weight: bold; width: 100%; padding: 10px 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; animation: pulseArcadeGame 3s infinite alternate; }
    .dropdown-trigger-btn i.arrow-icon { transition: transform 0.3s ease; font-size: 12px; margin-right: auto; padding-left: 5px; }
    .dropdown-trigger-btn.open-state i.arrow-icon { transform: rotate(180deg); }
    
    .dropdown-content-panel { display: none; background: #05070b; border: 1px solid #21262d; border-radius: 8px; padding: 4px 12px; margin-bottom: 10px; flex-direction: column; }
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 9px 0; display: block; transition: 0.15s ease; width: 100%; text-align: right; font-weight: 500; border-bottom: 1px dashed #161b22; }
    .game-link-btn:last-child { border-bottom: none; }
    .game-link-btn:hover { padding-right: 6px; text-shadow: 0 0 10px currentColor; }
    
    /* 💓 سحر التوهج النبضي المتدرج للأزرار كضربات القلب السيبرانية (Gradient Neon Pulse) */
    .general-link-item { text-decoration: none; font-size: 15.5px; font-weight: bold; padding: 11px 0; display: block; font-family: inherit; transition: transform 0.2s; }
    .general-link-item:hover { transform: translateX(-4px); }
    
    .link-home { color: #8b949e; animation: pulseHome 4s infinite alternate; }
    .link-projects { color: #a371f7; animation: pulseProjects 3.5s infinite alternate; }
    .link-about { color: #ff7b72; animation: pulseAbout 3.8s infinite alternate; }
    .link-scripts { color: #58a6ff; animation: pulseScripts 3.2s infinite alternate; }
    .link-report { color: #ff5555; animation: pulseReport 2.8s infinite alternate; }
    .link-telegram { color: #388bfd; border-bottom: none; animation: pulseTelegram 4.2s infinite alternate; }
    
    @keyframes pulseHome { 0% { text-shadow: 0 0 4px rgba(255,255,255,0.2); color: #8b949e; } 100% { text-shadow: 0 0 14px #ffffff; color: #ffffff; } }
    @keyframes pulseArcadeGame { 0% { text-shadow: 0 0 4px rgba(63,185,80,0.2); color: #3fb950; } 100% { text-shadow: 0 0 15px #3fb950, 0 0 25px #ff007f; color: #ff007f; } }
    @keyframes pulseProjects { 0% { text-shadow: 0 0 4px rgba(163,113,247,0.2); color: #a371f7; } 100% { text-shadow: 0 0 14px #a371f7, 0 0 22px #00f0f0; color: #00f0f0; } }
    @keyframes pulseAbout { 0% { text-shadow: 0 0 4px rgba(255,123,114,0.2); color: #ff7b72; } 100% { text-shadow: 0 0 14px #ff7b72; color: #ff5555; } }
    @keyframes pulseScripts { 0% { text-shadow: 0 0 4px rgba(88,166,255,0.2); color: #58a6ff; } 100% { text-shadow: 0 0 14px #58a6ff, 0 0 20px #3fb950; color: #3fb950; } }
    @keyframes pulseReport { 0% { text-shadow: 0 0 4px rgba(255,85,85,0.2); color: #ff5555; } 100% { text-shadow: 0 0 16px #ff0000; color: #fff; } }
    @keyframes pulseTelegram { 0% { text-shadow: 0 0 4px rgba(56,139,253,0.2); color: #388bfd; } 100% { text-shadow: 0 0 14px #388bfd; color: #58a6ff; } }
    
    @media (max-width: 850px) {
        .cyber-profile-cover { height: 220px; padding-bottom: 15px; } .cover-brand-name { font-size: 36px; }
        .profile-meta-row { flex-direction: column; align-items: center; text-align: center; margin-top: -75px; padding: 0 15px; }
        .profile-identity-zone { text-align: center; padding-bottom: 0; } .user-full-name { justify-content: center; flex-direction: column; gap: 4px; }
        .meta-info-grid { grid-template-columns: 1fr; }
    }
</style>
"""
# 🪐 الجزء الرابع: محرك التوليد التلقائي لـ الألعاب المبرأة تماماً من الـ n\ لتسليط الألوان حياً بداخل المنسدل
def get_embedded_games_html():
    import os
    from flask import current_app
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
        games_list_nodes = ['<p style="color:#8b949e; font-size:12px;">خطأ في تحميل باقة ألعاب النظام.</p>']
    return "".join(games_list_nodes) if games_list_nodes else '<p style="color:#8b949e; font-size:12px;">قائمة الألعاب فارغة.</p>'

@home_blueprint.route('/')
def home_page():
    dynamic_games_html = get_embedded_games_html()
    
    HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>علي احمد البراوي | الواجهة القياسية المعتمدة</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + HOME_CSS_PART1 + HOME_CSS_PART2 + HOME_CSS_PART3 + """
</head>
<body>

    <div class="top-nav">
        <a href="/" class="brand-logo">Albrawe</a>
        <!-- دالة التحكم اللحظي الصافي لفتح الستارة فورا وبدون وميض أو تحميل معلق -->
        <button class="menu-btn-trigger" onclick="toggleSidebarMenu(true)"><i class="fas fa-bars"></i> القائمة</button>
    </div>

    <!-- 🕹️ الـ Sidebar المنزلق الملوّن والمحمي المدمج صراحة لمنع التعليق البصري نهائياً -->
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
            
            <div class="section-menu-divider">مسارات إضافية</div>
            <a href="/projects" class="general-link-item link-projects">معرض المشاريع 📁</a>
            <a href="/about" class="general-link-item link-about">(About us) 👤</a>
            <a href="/scripts" class="general-link-item link-scripts">إسكربتات بايثون 💻</a>
            <a href="/report" class="general-link-item link-report">الإبلاغ عن مشكلة (صيانة) 🛠️</a>
            <a href="https://t.me" target="_blank" class="general-link-item link-telegram">حسابي في التليجرام ✈️</a>
        </div>
    </div>

    <div class="profile-master-container">
        <!-- الغلاف المطور المزود بمعرف الخلفية القوطية المحمي -->
        <div class="cyber-profile-cover" id="dynamicGothicCover">
            <h2 class="cover-brand-name">ALBRAWE</h2>
        </div>
        
        <div class="profile-meta-row">
            <div class="avatar-wrapper-circle">
                <img class="avatar-img-circle" id="userProfileAvatar" src="/static/avatar.png" alt="علي احمد البراوي" onerror="handleAvatarImageError(this)">
            </div>
            
                <div class="user-full-name">
                    <span>علي احمد البراوي</span>
                    <span class="user-slug-name">(Albrawe)</span>
                </div>
                <div class="followers-badge-line">
                    المتابعون <span class="followers-count">١٧١</span> • يتابع <span class="followers-count">١٥٧</span>
                </div>
            </div>
        </div>
        
        <div class="info-dashboard-card">
            <div class="dashboard-title-row"><i class="fas fa-info-circle"></i> لوحة المعلومات والنبذة التعريفية المعتمدة</div>
            <div class="meta-info-grid">
                <div class="info-item-box"><i class="fas fa-briefcase"></i><span>منشئ محتوى رقمي حياً بـ Cairo • عمل حر 💼</span></div>
                <div class="info-item-box"><i class="fas fa-graduation-cap"></i><span>درس في <span class="highlight-text-blue">Ain Shams University</span> 🎓</span></div>
                <div class="info-item-box"><i class="fas fa-school"></i><span>درس في <span style="color:#fff; font-weight:bold;">ابن خلدون الثانوية</span> 🏫</span></div>
                <div class="info-item-box" style="border-top:1px dashed var(--border-sub); padding-top:12px; grid-column:1/-1;">
                    <i class="fas fa-user-shield" style="color:#3fb950;"></i>
                    <span><strong style="color:#fff;">نبذة برمجية:</strong> هندسة وتطوير تطبيقات الويب الكاملة باستخدام بايثون (Flask)، وتصميم الواجهات المتكاملة والمعالجات المحلية الفائقة الكفاءة لعام 2026.</span>
                </div>
            </div>
        </div>
    </div>

    <div class="global-footer-bar">حقوق النشر محفوظة برمجياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©</div>

    <script>
        document.addEventListener("DOMContentLoaded", () => {
            const coverZone = document.getElementById("dynamicGothicCover");
            const imgChecker = new Image();
            imgChecker.src = "/static/lion-gothic.jpg";
            imgChecker.onload = () => {
                coverZone.style.backgroundImage = "linear-gradient(to bottom, rgba(6,9,13,0.3) 0%, #0d1117 100%), url('/static/lion-gothic.jpg')";
            };
            imgChecker.onerror = () => {
                coverZone.style.backgroundImage = "linear-gradient(to bottom, rgba(6,9,13,0.3) 0%, #0d1117 100%), url('/static/lion-gothic.JPG')";
            };
        });

        function handleAvatarImageError(imgNode) {
            if (!imgNode.dataset.triedUpper) {
                imgNode.dataset.triedUpper = "true";
                imgNode.src = "/static/avatar.PNG";
            } else {
                imgNode.src = "https://flagcdn.com";
            }
        }

        function toggleSidebarMenu(openState) {
            const sidebar = document.getElementById("slidingSidebarMenu");
            if (sidebar) {
                if(openState) sidebar.classList.add("active");
                else sidebar.classList.remove("active");
            }
        }

        function toggleGamesDropdown() {
            const trigger = document.getElementById("gamesMenuTrigger");
            const panel = document.getElementById("gamesDropdownPanel");
            if (panel.style.display === "flex") { panel.style.display = "none"; trigger.classList.remove("open-state"); }
            else { panel.style.display = "flex"; trigger.classList.add("open-state"); }
        }
    </script>
</body>
</html>
"""
    return render_template_string(HOME_HTML)
