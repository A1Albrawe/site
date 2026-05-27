from flask import Blueprint, request, jsonify, render_template_string, session, redirect, abort

admin_blueprint = Blueprint('admin', __name__)

# 🔒 بيانات اعتماد لوحة الإدارة الحصينة ومفاتيح عبور الرادار لعام 2026
ADMIN_USER = "albrawe"
ADMIN_PASS = "PASS2026"
SECRET_GATE_KEY = "open_gate_key_final_2026"

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>لوحة التحليلات والرقابة السيبرانية | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --bg-global: #06090d; --text-main: #c9d1d9; --bg-card: #0d1117; --border-main: #30363d; --border-neon: #58a6ff; --text-white: #fff; --border-sub: #21262d; }
        [data-theme="light"] { --bg-global: #f6f8fa; --text-main: #24292f; --bg-card: #ffffff; --border-main: #d0d7de; --border-neon: #0969da; --text-white: #1f2328; --border-sub: #d0d7de; }
        
        body { font-family: 'Courier New', Courier, monospace; background: var(--bg-global); color: var(--text-main); padding: 15px; margin: 0; box-sizing: border-box; transition: 0.3s; }
        .container { width: 100%; max-width: 1440px; margin: 0 auto; }
        
        .main-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border-sub); padding-bottom: 12px; margin-bottom: 20px; }
        @media (max-width: 600px) { .main-header { flex-direction: column; gap: 10px; text-align: center; } }
        
        .logout-btn { background: #f85149; color: #fff; border: none; padding: 7px 14px; border-radius: 6px; cursor: pointer; font-weight: bold; text-decoration: none; font-family: inherit; font-size: 12px; transition: 0.2s; }
        .logout-btn:hover { background: #da3633; box-shadow: 0 0 10px #f85149; }
        
        .complaints-inbox-card { background: var(--bg-card); border: 1px solid var(--border-main); border-top: 4px solid #f85149; border-radius: 12px; padding: 15px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(248,81,73,0.04); }
        .complaints-grid { display: flex; flex-direction: column; gap: 8px; max-height: 150px; overflow-y: auto; }
        .report-txt { font-size: 12px; display: flex; justify-content: space-between; padding: 6px; border-bottom: 1px dashed var(--border-sub); }
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 20px; }
        .stat-box { background: var(--bg-card); border: 1px solid var(--border-main); padding: 15px 10px; border-radius: 10px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .stat-box h5 { margin: 0 0 4px 0; color: var(--text-main); font-size: 12px; font-weight: bold; }
        .stat-box p { margin: 0; font-size: 20px; font-weight: bold; color: var(--border-neon); font-family: monospace; }
        .sub-stat-label { display: block; font-size: 11px; color: var(--text-main); margin-top: 6px; border-top: 1px dashed var(--border-sub); padding-top: 4px; }
        
        .section-title { color: #79c0ff; margin: 20px 0 10px 0; font-size: 15px; border-bottom: 2px solid var(--border-sub); padding-bottom: 6px; text-align: right; display: flex; align-items: center; gap: 6px; }
        .section-title.live { color: #3fb950; }
        .section-title.archive { color: var(--text-main); }
        
        .cards-mesh { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; margin-bottom: 25px; }
        
        .user-panel-card { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 10px; padding: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); display: flex; flex-direction: column; gap: 8px; text-align: right; font-size: 12px; }
        .user-panel-card.live-border { border-right: 5px solid #3fb950; }
        .user-panel-card.archive-border { border-right: 5px solid var(--border-main); opacity: 0.9; }
        .card-top-info { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-sub); padding-bottom: 6px; }
        .card-username { font-size: 13px; font-weight: bold; color: var(--text-white); }
        .card-device { font-size: 11px; color: #ffd700; font-weight: bold; }
        
        .card-meta-line { display: flex; align-items: center; gap: 6px; color: var(--text-main); }
        .card-meta-line i { color: var(--text-main); width: 16px; text-align: center; }
        
        .flag-img { width: 16px; height: 12px; border-radius: 2px; object-fit: cover; }
        .time-badge { color: var(--border-neon); font-weight: bold; background: rgba(88,166,255,0.05); padding: 2px 5px; border-radius: 4px; border: 1px solid var(--border-main); font-family: monospace; }
        .games-total-badge { color: #3fb950; font-weight: bold; background: rgba(63,185,80,0.05); padding: 2px 5px; border-radius: 4px; border: 1px solid var(--border-main); font-family: monospace; }
        
        .drop-trigger-btn { background: var(--bg-global); border: 1px solid var(--border-main); color: var(--text-main); width: 100%; padding: 6px; border-radius: 6px; cursor: pointer; font-size: 11.5px; font-weight: bold; text-align: right; display: flex; justify-content: space-between; align-items: center; font-family: inherit; }
        .drop-trigger-btn:hover { border-color: var(--border-neon); color: var(--text-white); }
        
        .drop-content-panel { display: none; background: var(--bg-global); border: 1px solid var(--border-sub); padding: 8px; border-radius: 6px; margin-top: 2px; }
        .route-path-box { font-size: 11px; color: #a371f7; line-height: 1.5; word-break: break-all; }
        
        .games-dashboard { display: grid; grid-template-columns: repeat(2, 1fr); gap: 4px; }
        .mini-game-tag { font-size: 10.5px; display: flex; justify-content: space-between; padding: 4px; background: var(--bg-card); border-radius: 4px; border: 1px solid var(--border-main); font-family: monospace; }
        
        .clear-db-btn { background: var(--bg-card); border: 1px solid #d29922; color: #d29922; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-weight: bold; font-family: inherit; font-size: 11.5px; }
    </style>
    <script>
        (function() { const savedTheme = localStorage.getItem("albrawe_global_theme_mode") || "dark"; document.documentElement.setAttribute("data-theme", savedTheme); })();
    </script>
</head>
<body>
    <div class="container">
        <div class="main-header">
            <h2 style="margin:0; color:var(--text-white);"><i class="fas fa-chart-network" style="color:#a371f7; margin-left:6px;"></i> رادار الرقابة والتحليلات المطور V3</h2>
            <div style="display:flex; gap:10px; align-items:center;">
                <button class="clear-db-btn" onclick="clearLogsDatabase()"><i class="fas fa-trash-alt"></i> تصفير السجلات</button>
                <a href="/albrawe-admin-panel-2026/logout" class="logout-btn">تسجيل الخروج 🚪</a>
            </div>
        </div>
        
        <div class="complaints-inbox-card">
            <h3 style="margin:0; color:#ff7b72; font-size:14px; border-bottom:1px solid var(--border-sub); padding-bottom:6px;"><i class="fas fa-envelope-open-text"></i> صندوق الشكاوى وبلاغات الصيانة المدمج بالهوية</h3>
            <div class="complaints-grid" id="globalComplaintsInbox"></div>
        </div>

        <div class="grid-stats">
            <div class="stat-box" style="border-top: 3px solid #58a6ff;"><h5>الزيارات النشطة حالياً</h5><p id="totalViews">0</p></div>
            <div class="stat-box" style="border-top: 3px solid #d29922;"><h5>إجمالي زيارات الموقع الكلية</h5><p id="historicalViews" style="color: #d29922;">0</p></div>
            <div class="stat-box" style="border-top: 3px solid #3fb950;">
                <h5 style="color: #3fb950;">مجموع وقت الاستخدام للزوار</h5>
                <p id="totalGlobalUsageTime" style="color: #3fb950;">0 ثانية</p>
                <span class="sub-stat-label" id="avgUsageTime">متوسط الاستخدام الفردي: 0 ثانية</span>
            </div>
            <div class="stat-box" style="border-top: 3px solid #f85149;"><h5>إجمالي بلاغات الصيانة</h5><p id="totalComplaints" style="color: #f85149;">0</p></div>
        </div>
        
        <h3 class="section-title live"><i class="fas fa-broadcast-tower"></i> الرصد اللحظي النشط (الموجودين بالموقع حالياً)</h3>
        <div class="cards-mesh" id="liveCardsContainer"></div>
        
        <h3 class="section-title archive"><i class="fas fa-history"></i> سجل ومستودع الزوار المغادرين التاريخي</h3>
        <div class="cards-mesh" id="archiveCardsContainer"></div>
    </div>
    <script>
        const BarkCardDropdown = (panelId) => {
            const panel = document.getElementById(panelId);
            panel.style.display = (panel.style.display === 'block') ? 'none' : 'block';
        }

        function formatFriendlyTime(totalSeconds) {
            if (totalSeconds <= 0 || isNaN(totalSeconds)) return "0 ثانية";
            let years = Math.floor(totalSeconds / (365 * 24 * 3600));
            let remainder = totalSeconds % (365 * 24 * 3600);
            let months = Math.floor(remainder / (30 * 24 * 3600));
            remainder = remainder % (30 * 24 * 3600);
            let days = Math.floor(remainder / (24 * 3600));
            remainder = remainder % (24 * 3600);
            let hours = Math.floor(remainder / 3600);
            remainder = remainder % 3600;
            let minutes = Math.floor(remainder / 60);
            let seconds = remainde        function fetchAndRenderAnalytics() {
            fetch('/api/admin_get_all_data')
            .then(res => res.json())
            .then(data => {
                let liveDB = data.analytics || [];
                let complDB = data.reports || [];
                let historicalCount = data.historicalVisits || 0;
                let archiveDB = JSON.parse(localStorage.getItem('permanent_archive_db') || "[]");
                
                liveDB.forEach(liveUser => {
                    let existingIndex = archiveDB.findIndex(archiveUser => archiveUser.username === liveUser.username);
                    if (existingIndex !== -1) {
                        let currentStep = 'الرئيسية 🏠';
                        if (liveUser.snakeTime > 0) currentStep = 'لعبة الثعبان 🐍';
                        else if (liveUser.tetrisTime > 0) currentStep = 'لعبة التترس 🧱';
                        else if (liveUser.xoTime > 0) currentStep = 'لعبة X-O ❌';
                        else if (liveUser.shooterTime > 0) currentStep = 'قاصف الفضاء 🚀';
                        else if (liveUser.clickerTime > 0) currentStep = 'تحدي النقر ⚡';
                        else if (liveUser.cardTime > 0) currentStep = 'لعبة البطاقات 🃏';
                        
                        let historyArray = archiveDB[existingIndex].browsingHistory || ["الرئيسية 🏠"];
                        if (historyArray[historyArray.length - 1] !== currentStep) { historyArray.push(currentStep); }
                        liveUser.browsingHistory = historyArray;
                        archiveDB[existingIndex] = liveUser;
                    } else {
                        liveUser.browsingHistory = ["الرئيسية 🏠"]; archiveDB.push(liveUser);
                    }
                });
                localStorage.setItem('permanent_archive_db', JSON.stringify(archiveDB));

                let lastSavedHistorical = parseInt(localStorage.getItem('backup_historical') || "0");
                if (historicalCount > lastSavedHistorical) { localStorage.setItem('backup_historical', historicalCount); } else { historicalCount = lastSavedHistorical; }
                if (historicalCount < archiveDB.length) { historicalCount = archiveDB.length; localStorage.setItem('backup_historical', historicalCount); }
                
                document.getElementById('totalViews').innerText = liveDB.length;
                document.getElementById('historicalViews').innerText = historicalCount;
                document.getElementById('totalComplaints').innerText = complDB.length;
                
                let totalSeconds = 0;
                archiveDB.forEach(item => { totalSeconds += (item.duration || 0); });
                document.getElementById('totalGlobalUsageTime').innerText = formatFriendlyTime(totalSeconds);
                let avgCalc = archiveDB.length > 0 ? Math.round(totalSeconds / archiveDB.length) : 0;
                document.getElementById('avgUsageTime').innerText = "متوسط الاستخدام الفردي: " + formatFriendlyTime(avgCalc);
                
                let inboxHtml = "";
                if(complDB.length === 0) { inboxHtml = '<p style="color:var(--text-main); font-size:12px; text-align:center; margin:5px 0;">الصندوق نظيف ومبرأ كلياً.</p>'; } else {
                    complDB.forEach(c => {
                        inboxHtml += '<div class="report-txt"><span><i class="fas fa-user-tag" style="color:var(--border-neon);"></i> <strong>' + c.user + '</strong>: ' + c.details + '</span><span style="color:var(--border-neon);">' + c.date + '</span></div>';
                    });
                }
                document.getElementById('globalComplaintsInbox').innerHTML = inboxHtml;
                
                let liveCardsHtml = ""; let archiveCardsHtml = "";
                if(archiveDB.length > 0) {
                    archiveDB.slice().reverse().forEach(user => {
                        let snake = user.snakeTime || 0; let tetris = user.tetrisTime || 0; let xo = user.xoTime || 0; let shooter = user.shooterTime || 0; let clicker = user.clickerTime || 0; let card = user.cardTime || 0;
                        let totalGamesSeconds = snake + tetris + xo + shooter + clicker + card;
                        let currentLoc = user.location || "القاهرة - مصر";
                        let countryCode = "eg"; if (currentLoc.toLowerCase().includes("saudi")) countryCode = "sa";
                        
                        let flagImgHtml = '<img class="flag-img" src="https://flagcdn.com' + countryCode + '.png" alt="Flag">';
                        let stepsList = user.browsingHistory || ["الرئيسية 🏠"];
                        let isUserStillLive = liveDB.some(l => l.username === user.username);
                        let cardIdSuffix = user.username.replace(/[^a-zA-Z0-9]/g, '');
                        let pathPanelId = 'pathPanel_' + cardIdSuffix;
                        let gamesPanelId = 'gamesPanel_' + cardIdSuffix;
                        
                        let cardBodyHtml = '<div class="user-panel-card ' + (isUserStillLive ? 'live-border' : 'archive-border') + '">' +
                            '<div class="card-top-info"><span class="card-username"><i class="fas fa-user-circle"></i> ' + user.username + '</span><span class="card-device">' + (user.deviceModel || 'Android Device 📱') + '</span></div>' +
                            '<div class="card-meta-line"><i class="fas fa-map-marker-alt"></i> ' + flagImgHtml + ' <span style="color:#3fb950; font-weight:bold;">' + currentLoc + '</span></div>' +
                            '<div class="card-meta-line"><i class="fas fa-clock"></i> <span>الدخول: ' + user.loginTime + '</span></div>' +
                            '<div class="card-meta-line"><i class="fas fa-browser"></i> <span>الموقع: <span class="time-badge">' + formatFriendlyTime(user.duration || 0) + '</span> | الألعاب: <span class="games-total-badge">' + formatFriendlyTime(totalGamesSeconds) + '</span></span></div>' +
                            '<button class="drop-trigger-btn" onclick="BarkCardDropdown(\'' + pathPanelId + '\')"><span><i class="fas fa-map-signs"></i> مسار التنقل والصفحات</span> <i class="fas fa-chevron-down"></i></button>' +
                            '<div class="drop-content-panel" id="' + pathPanelId + '"><div class="route-path-box">' + stepsList.join(' ➔ ') + '</div></div>' +
                            '<button class="drop-trigger-btn" onclick="BarkCardDropdown(\'' + gamesPanelId + '\')"><span><i class="fas fa-gamepad"></i> عدادات الستة ألعاب الفرعية</span> <i class="fas fa-chevron-down"></i></button>' +
                            '<div class="drop-content-panel" id="' + gamesPanelId + '">' +
                                '<div class="games-dashboard">' +
                                    '<div class="mini-game-tag" style="color:#3fb950;"><span>🐍 ثعبان</span><span>' + formatFriendlyTime(snake) + '</span></div>' +
                                    '<div class="mini-game-tag" style="color:#d29922;"><span>🧱 تترس</span><span>' + formatFriendlyTime(tetris) + '</span></div>' +
                                    '<div class="mini-game-tag" style="color:#a371f7;"><span>❌ X-O</span><span>' + formatFriendlyTime(xo) + '</span></div>' +
                                    '<div class="mini-game-tag" style="color:#388bfd;"><span>🚀 فضاء</span><span>' + formatFriendlyTime(shooter) + '</span></div>' +
                                    '<div class="mini-game-tag" style="color:#ff7b72;"><span>⚡ نقر</span><span>' + formatFriendlyTime(clicker) + '</span></div>' +
                                    '<div class="mini-game-tag" style="color:#58a6ff;"><span>🃏 بطاقات</span><span>' + formatFriendlyTime(card) + '</span></div>' +
                                '</div>' +
                            '</div>' +
                        '</div>';
                        if(isUserStillLive) liveCardsHtml += cardBodyHtml; else archiveCardsHtml += cardBodyHtml;
                    });
                }
                if(liveCardsHtml === "") liveCardsHtml = '<p style="grid-column:1/-1; text-align:center; color:var(--text-main); font-size:12px;">لا توجد أي زيارات نشطة حالياً. 🛰></p>';
                if(archiveCardsHtml === "") archiveCardsHtml = '<p style="grid-column:1/-1; text-align:center; color:var(--text-main); font-size:12px;">لا توجد سجلات مغادرين.</p>';
                document.getElementById('liveCardsContainer').innerHTML = liveCardsHtml;
                document.getElementById('archiveCardsContainer').innerHTML = archiveCardsHtml;
            });
        }
        function clearLogsDatabase() { if(confirm("هل أنت متأكد من مسح الأرشيف التراكمي وتصفير السجلات بالكامل؟")) { localStorage.removeItem('permanent_archive_db'); localStorage.removeItem('backup_historical'); fetch('/api/admin_clear_data', { method: 'POST' }).then(() => fetchAndRenderAnalytics()); } }
        fetchAndRenderAnalytics(); setInterval(fetchAndRenderAnalytics, 4000);
    </script>
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل دخول الإدارة | Albrawe</title>
    <style>
        body { font-family: monospace; background: #0d1117; color: #c9d1d9; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .login-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #f85149; padding: 30px; border-radius: 12px; width: 100%; max-width: 360px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
        .form-group { margin-bottom: 15px; display: flex; flex-direction: column; gap: 6px; text-align: right; }
        input { padding: 10px; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #fff; font-family: inherit; width: 100%; box-sizing: border-box; }
        input:focus { border-color: #f85149; outline: none; }
        .btn { background: #f85149; color: #fff; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; font-family: inherit; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-card">
        <h3 style="margin-top:0; text-align:center; color:#fff;">🔐 نظام تفتيش الإدارة السرية</h3>
        <form method="POST" action="/albrawe-admin-panel-2026">
            <div class="form-group">
                <label>اسم المسؤول:</label>
                <input type="text" name="username" required autocomplete="off">
            </div>
            <div class="form-group">
                <label>كلمة المرور التكتيكية:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn">تأكيد الهوية البيومترية 🛡️</button>
        </form>
    </div>
</body>
</html>
"""

@admin_blueprint.route('/', methods=['GET', 'POST'])
@admin_blueprint.route('/albrawe-admin-panel-2026', methods=['GET', 'POST'])
def admin_page():
    gate_key = request.args.get('key', '')
    if request.method == 'POST':
        user = request.form.get('username')
        passwd = request.form.get('password')
        if user == ADMIN_USER and passwd == ADMIN_PASS:
            session['admin_logged_in'] = True
            session['gate_key_authenticated'] = True
            return render_template_string(ADMIN_HTML)
        else:
            return render_template_string(LOGIN_HTML + "<script>alert('❌ خطأ فادح: بيانات الاعتماد غير صحيحة!');</script>")
    if session.get('admin_logged_in') and session.get('gate_key_authenticated'):
        return render_template_string(ADMIN_HTML)
    if gate_key == SECRET_GATE_KEY:
        session['gate_key_authenticated'] = True
        return render_template_string(LOGIN_HTML)
    abort(404)

@admin_blueprint.route('/albrawe-admin-panel-2026/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('gate_key_authenticated', None)
    return redirect('/')
eParts.push(months + " شهر");
            if (days > 0) timeParts.push(days + " يوم");
            if (hours > 0) timeParts.push(hours + " ساعة");
            if (minutes > 0) timeParts.push(minutes + " دقيقة");
            if (seconds > 0 || timeParts.length === 0) timeParts.push(seconds + " ثانية");
            return timeParts.join(" و ");
        }
