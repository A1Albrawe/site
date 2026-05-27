from flask import Blueprint, render_template_string

report_blueprint = Blueprint('report', __name__)

REPORT_CSS = """
<style>
    body { font-family: 'Courier New', Courier, monospace; background: var(--bg-global, #06090d); color: var(--text-main, #c9d1d9); margin: 0; padding: 25px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; overflow-x: hidden; }
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 600px; margin: 0 auto 35px auto; border-bottom: 2px solid var(--border-sub, #21262d); padding-bottom: 14px; box-sizing: border-box; }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white, #fff); text-shadow: 0 0 8px var(--border-neon, #58a6ff); font-family: monospace; text-decoration: none; cursor: pointer; }
    .menu-btn-trigger { background: var(--bg-card, #0d1117); border: 1px solid var(--border-main, #30363d); color: var(--border-neon, #58a6ff); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 6px; font-family: inherit; }
    .menu-btn-trigger:hover { background: var(--border-neon, #58a6ff); color: var(--bg-global, #06090d); box-shadow: 0 0 12px var(--border-neon, #58a6ff); }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
    .form-box { background: var(--bg-card, #0d1117); border: 1px solid var(--border-main, #30363d); border-radius: 14px; width: 100%; max-width: 440px; padding: 30px 25px; box-shadow: 0 25px 50px rgba(0,0,0,0.5); border-bottom: 4px solid #ff7b72; box-sizing: border-box; text-align: right; }
    
    .form-group { margin-bottom: 18px; display: flex; flex-direction: column; gap: 6px; }
    .form-group label { font-size: 13.5px; font-weight: bold; color: var(--text-white, #fff); }
    .form-control { padding: 11px; background: var(--bg-global, #06090d); border: 1px solid var(--border-main, #30363d); border-radius: 6px; color: #fff; font-family: inherit; font-size: 13.5px; width: 100%; box-sizing: border-box; }
    .form-control:focus { border-color: #ff7b72; outline: none; box-shadow: 0 0 8px rgba(255,123,114,0.15); }
    
    .submit-btn { background: #161b22; border: 1px solid #ff7b72; color: #ff7b72; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; font-family: inherit; width: 100%; font-size: 14px; transition: 0.2s; margin-top: 5px; }
    .submit-btn:hover { background: #ff7b72; color: #06090d; box-shadow: 0 0 15px #ff7b72; }
    
    .global-footer-bar { width: 100%; text-align: center; margin-top: 40px; padding-top: 15px; border-top: 1px solid var(--border-sub, #21262d); font-size: 12px; color: #8b949e; font-family: monospace; }
</style>
"""

REPORT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>الإلاغ عن مشكلة صيانة | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + REPORT_CSS + """
    <script>
        (function() {
            const savedTheme = localStorage.getItem("albrawe_global_theme_mode") || "dark";
            document.documentElement.setAttribute("data-theme", savedTheme);
        })();
    </script>
</head>
<body>

    <div class="top-nav">
        <a href="/" class="brand-logo">Albrawe</a>
        <button class="menu-btn-trigger" onclick="loadAndOpenSidebarMenu()"><i class="fas fa-bars"></i> القائمة</button>
    </div>

    <div id="dynamicMenuInjectionZone"></div>

    <div class="main-container">
        <div class="form-box">
            <h3 style="margin-top:0; color:#ff7b72; font-size:17px; text-align:center;"><i class="fas fa-tools"></i> نظام إيداع بلاغات الصيانة</h3>
            <p style="font-size:11.5px; color:#8b949e; text-align:center; margin-bottom:20px;">قم بتعبئة حقول الهوية لشرح العطل الفني المكتشف:</p>
            
            <div class="form-group">
                <label>الاسم المميز لمرسل البلاغ:</label>
                <input type="text" id="complaintUserField" class="form-control" placeholder="اكتب اسمك الفريد هنا..." autocomplete="off">
            </div>
            
            <div class="form-group">
                <label>تفاصيل وشرح عطل صيانة السيرفر:</label>
                <textarea id="complaintDetailsField" class="form-control" rows="4" placeholder="اشرح المشكلة التقنية بالتفصيل..." style="resize:none;"></textarea>
            </div>
            
            <button class="submit-btn" onclick="executeComplaintSubmission()"><i class="fas fa-paper-plane"></i> إرسال البلاغ فوراً للمسؤول</button>
        </div>
    </div>

    <div class="global-footer-bar">
        حقوق النشر محفوظة برمجياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©
    </div>

    <script>
        function executeComplaintSubmission() {
            const user = document.getElementById("complaintUserField").value.strip || document.getElementById("complaintUserField").value;
            const details = document.getElementById("complaintDetailsField").value.strip || document.getElementById("complaintDetailsField").value;
            
            if(!user || !details) { alert("❌ خطأ: يرجى كتابة الاسم وشرح المشكلة أولاً!"); return; }
            
            fetch('/api/submit_complaint', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ user: user, details: details })
            })
            .then(res => {
                if(res.ok) {
                    alert("🟢 تم إرسال بلاغ الصيانة بنجاح وحقن اسمك المميز بداخل الرادار حياً!");
                    document.getElementById("complaintUserField").value = "";
                    document.getElementById("complaintDetailsField").value = "";
                } else { alert("❌ خطأ: فشل إيداع البلاغ في قاعدة المزامنة السحابية."); }
            }).catch(() => { alert("❌ خطأ: تعذر الاتصال بـ خادم الـ API."); });
        }

        function loadAndOpenSidebarMenu() {
            const zone = document.getElementById("dynamicMenuInjectionZone");
            if (zone.innerHTML.trim() !== "") { toggleSidebarMenu(true); updateThemeButtonTextOnSidebar(); return; }
            fetch('/api/get_sidebar_menu').then(res => res.json()).then(data => {
                const styleNode = document.createElement("style");
                styleNode.innerHTML = data.css; document.head.appendChild(styleNode);
                zone.innerHTML = data.html; updateThemeButtonTextOnSidebar();
                setTimeout(() => { toggleSidebarMenu(true); }, 30);
            });
        }
        function toggleSidebarMenu(openState) { const sidebar = document.getElementById("slidingSidebarMenu"); if (sidebar) { if(openState) sidebar.classList.add("active"); else sidebar.classList.remove("active"); } }
        function toggleGamesDropdown() { const trigger = document.getElementById("gamesMenuTrigger"); const panel = document.getElementById("gamesDropdownPanel"); if (panel.style.display === "flex") { panel.style.display = "none"; trigger.classList.remove("open-state"); } else { panel.style.display = "flex"; trigger.classList.add("open-state"); } }
        function toggleGlobalThemeMode() {
            const currentTheme = document.documentElement.getAttribute("data-theme") || "dark"; const newTheme = currentTheme === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", newTheme); localStorage.setItem("albrawe_global_theme_mode", newTheme);
            const sidebar = document.getElementById("slidingSidebarMenu");
            if(sidebar && newTheme === "light") {
                sidebar.style.setProperty("--bg-sidebar", "#ffffff"); sidebar.style.setProperty("--border-color", "#d0d7de"); sidebar.style.setProperty("--text-muted", "#57606a"); sidebar.style.setProperty("--bg-btn", "#f6f8fa"); sidebar.style.setProperty("--bg-dropdown", "#f6f8fa"); sidebar.style.setProperty("--text-general", "#24292f"); sidebar.style.setProperty("--border-dashed", "#d0d7de"); sidebar.style.setProperty("--text-home-btn", "#24292f"); sidebar.style.setProperty("--text-theme-btn", "#0969da");
            } else if(sidebar) {
                sidebar.style.removeProperty("--bg-sidebar"); sidebar.style.removeProperty("--border-color"); sidebar.style.removeProperty("--text-muted"); sidebar.style.removeProperty("--bg-btn"); sidebar.style.removeProperty("--bg-dropdown"); sidebar.style.removeProperty("--text-general"); sidebar.style.removeProperty("--border-dashed"); sidebar.style.removeProperty("--text-home-btn"); sidebar.style.removeProperty("--text-theme-btn");
            }
            updateThemeButtonTextOnSidebar();
        }
        function updateThemeButtonTextOnSidebar() { const btnText = document.getElementById("themeToggleTextBtn"); if (btnText) { const currentTheme = document.documentElement.getAttribute("data-theme") || "dark"; btnText.innerText = currentTheme === "dark" ? "الوضع الفاتح ⚪" : "الوضع الداكن ⚫"; } }
    </script>
</body>
</html>
"""

@report_blueprint.route('/report')
def report_page():
    return render_template_string(REPORT_HTML)
