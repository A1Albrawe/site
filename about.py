from flask import Blueprint, render_template_string

about_blueprint = Blueprint('about', __name__)

ABOUT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>About Us | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <style>
        :root { --bg-global: #06090d; --text-main: #c9d1d9; --bg-card: #0d1117; --border-main: #30363d; --border-neon: #58a6ff; --text-white: #fff; --border-sub: #21262d; }
        [data-theme="light"] { --bg-global: #f6f8fa; --text-main: #24292f; --bg-card: #ffffff; --border-main: #d0d7de; --border-neon: #0969da; --text-white: #1f2328; --border-sub: #d0d7de; }
        body { font-family: 'Courier New', monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 25px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; transition: 0.3s; }
        
        .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 800px; margin: 0 auto 35px auto; border-bottom: 2px solid var(--border-sub); padding-bottom: 14px; box-sizing: border-box; }
        .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 8px var(--border-neon); text-decoration: none; font-family: monospace; }
        .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; font-family: inherit; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
        .about-box { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 14px; padding: 35px; width: 100%; max-width: 600px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border-bottom: 4px solid var(--border-neon); box-sizing: border-box; text-align: right; }
        
        .highlight-title { font-size: 18px; color: var(--text-white); margin-top: 0; margin-bottom: 15px; border-bottom: 1px dashed var(--border-sub); padding-bottom: 8px; }
        .about-text { font-size: 14px; line-height: 1.7; color: var(--text-main); margin-bottom: 20px; }
        
        .global-footer-bar { width: 100%; text-align: center; margin-top: 40px; padding-top: 15px; border-top: 1px solid var(--border-sub); font-size: 12px; color: var(--text-main); font-family: monospace; }
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
    
    <div class="main-container">
        <div class="about-box">
            <h3 class="highlight-title"><i class="fas fa-user-shield" style="color:var(--border-neon); margin-left:6px;"></i> الهوية الرقمية للمنصة لعام 2026</h3>
            <p class="about-text">
                تم تأسيس وتطوير هذا الخادم السحابي المحصن كمنظومة متكاملة تجمع بين الفن المعماري القياسي وهندسة البرمجيات المتقدمة لتقديم بيئة أركيد نيونية متجاوبة حياً، مع تزويدها برادار رصد بياني فوري فائق الدقة.
            </p>
        </div>
    </div>
    
    <div class="global-footer-bar">حقوق النشر محفوظة برمجياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©</div>
    
    <script>
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

@about_blueprint.route('/about')
def about_page():
    return render_template_string(ABOUT_HTML)
