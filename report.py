from flask import Blueprint, render_template_string

report_blueprint = Blueprint('report', __name__)

REPORT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>البلاغات والصيانة | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <style>
        :root { --bg-global: #030508; --text-main: #c9d1d9; --bg-card: rgba(13, 17, 23, 0.9); --border-main: #21262d; --border-neon: #ff5555; --border-cyber: #ff007f; --text-white: #fff; --border-sub: #30363d; }
        body { font-family: 'Courier New', monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 25px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; position: relative; }
        
        .radar-background-grid { position: fixed; top: 50%; left: 50%; width: 140vw; height: 140vw; transform: translate(-50%, -50%); border-radius: 50%; border: 1px solid rgba(255, 85, 85, 0.08); pointer-events: none; z-index: 1; animation: radarRotate 25s linear infinite; }
        @keyframes radarRotate { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }

        .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 800px; margin: 0 auto 35px auto; border-bottom: 2px solid var(--border-sub); padding-bottom: 14px; box-sizing: border-box; position: relative; z-index: 100; }
        .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 10px var(--border-neon); text-decoration: none; font-family: monospace; }
        .menu-btn-trigger { background: #161b22; border: 1px solid var(--border-sub); color: var(--border-neon); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; font-family: inherit; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; position: relative; z-index: 10; }
        
        /* 🛠️ هندسة "واجهة شاشة الإدخال والاختراق السيبراني العسكري" (Command Line Breach Interface) */
        .form-box { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 14px; padding: 30px; width: 100%; max-width: 500px; box-shadow: 0 20px 50px rgba(255,0,0,0.1); border-bottom: 4px solid var(--border-neon); border-left: 4px solid var(--border-cyber); box-sizing: border-box; text-align: right; backdrop-filter: blur(10px); }
        .form-group { margin-bottom: 18px; display: flex; flex-direction: column; gap: 6px; }
        label { font-weight: bold; color: var(--text-white); font-size: 13.5px; font-family: monospace; letter-spacing: 0.5px; }
        
        /* إدخال نصوص تومض وتتوهج */
        input, textarea { padding: 12px; background: #04060a; border: 1px solid var(--border-main); border-radius: 6px; color: #ff5555; font-family: monospace; width: 100%; box-sizing: border-box; font-size: 13px; text-shadow: 0 0 5px rgba(255,85,85,0.5); box-shadow: inset 0 0 10px rgba(0,0,0,0.8); }
        input:focus, textarea:focus { border-color: var(--border-cyber); outline: none; box-shadow: 0 0 10px rgba(255,0,127,0.2); }
        
        .submit-btn { background: var(--border-neon); color: #fff; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; font-family: inherit; margin-top: 10px; font-size: 14px; transition: 0.2s; text-transform: uppercase; letter-spacing: 0.5px; }
        .submit-btn:hover { box-shadow: 0 0 15px var(--border-neon); background: var(--border-cyber); }
        .global-footer-bar { width: 100%; text-align: center; margin-top: 40px; padding-top: 15px; border-top: 1px solid var(--border-sub); font-size: 12px; color: #8b949e; font-family: monospace; position: relative; z-index: 100; }
    </style>
</head>
<body>
    <div class="radar-background-grid"></div>
    <div class="top-nav">
        <a href="/" class="brand-logo">Albrawe</a>
        <button class="menu-btn-trigger" onclick="loadAndOpenSidebarMenu()"><i class="fas fa-bars"></i> القائمة</button>
    </div>
    <div id="dynamicMenuInjectionZone"></div>
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
    <div class="global-footer-bar">حقوق النشر محفوظة برمجياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©</div>
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
                if(res.ok) { alert("🟢 INJECTION_SUCCESSFUL: تم استلام البلاغ وحقن الهوية في رادار الرصد بنجاح."); document.getElementById("reporterName").value=""; document.getElementById("complaintDetails").value=""; }
            }).catch(() => { alert("❌ CONNECTION_FAILED."); });
        }
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

@report_blueprint.route('/report')
def report_page():
    return render_template_string(REPORT_HTML)
