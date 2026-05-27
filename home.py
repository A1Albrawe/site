from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

# عزل التنسيقات الفخمة لحماية خوادم Flask من التداخل النصي للأقواس خارج الصندوق
HOME_CSS = """
<style>
    :root {
        --bg-global: #06090d; --text-main: #c9d1d9; --bg-card: #0d1117; 
        --border-main: #30363d; --border-neon: #58a6ff; --border-cyber: #3fb950; --text-white: #fff; --border-sub: #21262d;
    }
    
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 0; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; overflow-x: hidden; }
    
    /* 🌐 شريط التوجيه العلوي الموحد الثابت */
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1200px; margin: 0 auto; padding: 15px 25px; box-sizing: border-box; position: relative; z-index: 1000; border-bottom: 1px solid var(--border-sub); }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 8px var(--border-neon); text-decoration: none; font-family: monospace; cursor: pointer; }
    .menu-btn-trigger { background: var(--bg-card); border: 1px solid var(--border-main); color: var(--border-neon); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 6px; font-family: inherit; transition: 0.2s; }
    .menu-btn-trigger:hover { background: var(--border-neon); color: #000; box-shadow: 0 0 12px var(--border-neon); }
    
    .profile-master-container { width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 15px 40px 15px; box-sizing: border-box; position: relative; z-index: 10; }
    
    /* 🦁 هندسة ومحاكاة غلاف الأسد القوطي المظلم والاسم البرمي المتوهج (Gothic Lion Cover Header) بالبكسل حياً */
    .cyber-profile-cover { 
        width: 100%; height: 350px; 
        background: linear-gradient(to bottom, rgba(6,9,13,0.3) 0%, #0d1117 100%), url('/static/lion-gothic.jpg') no-repeat center center;
        background-size: cover; border-radius: 0 0 18px 18px; border: 1px solid var(--border-main); 
        border-bottom: 4px solid var(--border-neon); position: relative; 
        display: flex; flex-direction: column; align-items: center; justify-content: flex-end; padding-bottom: 30px; box-sizing: border-box;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6); 
    }
    .cover-brand-name { font-size: 55px; font-weight: 900; color: #fff; letter-spacing: 3px; font-family: 'Courier New', monospace; text-transform: uppercase; margin: 0; text-shadow: 0 0 12px #58a6ff, 0 0 25px rgba(88,166,255,0.5); }
    
    /* 🖼️ هندسة كرت الهوية الشخصية التفاعلي ومحاكاة الأفاتار الدائري التداخلي المتطابق */
    .profile-meta-row { display: flex; align-items: flex-end; gap: 30px; margin-top: -65px; padding: 0 40px; box-sizing: border-box; width: 100%; direction: rtl; position: relative; z-index: 100; transform-style: preserve-3d; transform: perspective(1000px); }
    .avatar-wrapper-circle { width: 155px; height: 155px; border-radius: 50%; border: 5px solid var(--bg-global); overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5); background: #04060a; flex-shrink: 0; transition: transform 0.25s ease; }
    .avatar-img-circle { width: 100%; height: 100%; object-fit: cover; }
    
    .profile-identity-zone { flex: 1; text-align: right; padding-bottom: 15px; }
    .user-full-name { font-size: 28px; font-weight: bold; color: var(--text-white); margin: 0 0 5px 0; display: flex; align-items: center; gap: 10px; }
    .user-slug-name { font-size: 18px; color: #8b949e; font-family: monospace; font-weight: 500; }
    .followers-badge-line { font-size: 13.5px; color: #8b949e; margin: 8px 0 0 0; font-weight: 500; }
    .followers-count { color: var(--text-white); font-weight: bold; }
    
    /* 🛠️ أجنحة لوحة المعلومات الموثقة لجامعة عين شمس والثانوية حياً */
    .info-dashboard-card { background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 14px; padding: 30px; margin-top: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); text-align: right; direction: rtl; box-sizing: border-box; border-right: 4px solid var(--border-cyber); }
    .dashboard-title-row { display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: bold; color: #58a6ff; margin-bottom: 20px; border-bottom: 1px solid var(--border-sub); padding-bottom: 10px; }
    
    .meta-info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
    .info-item-box { display: flex; align-items: center; gap: 12px; font-size: 14.5px; color: var(--text-main); line-height: 1.5; }
    .info-item-box i { color: #8b949e; width: 20px; text-align: center; font-size: 16px; }
    .highlight-text-blue { color: #58a6ff; font-weight: bold; text-decoration: none; }
    
    @media (max-width: 850px) {
        .cyber-profile-cover { height: 220px; padding-bottom: 15px; background-attachment: scroll; } .cover-brand-name { font-size: 36px; }
        .profile-meta-row { flex-direction: column; align-items: center; text-align: center; margin-top: -75px; padding: 0 15px; transform: none !important; }
        .profile-identity-zone { text-align: center; padding-bottom: 0; } .user-full-name { justify-content: center; flex-direction: column; gap: 4px; }
        .meta-info-grid { grid-template-columns: 1fr; }
    }
</style>
"""
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>علي احمد البراوي | البوابة المعمارية والبرمجية</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + HOME_CSS + """
</head>
<body>

    <div class="top-nav">
        <a href="/" class="brand-logo">Albrawe</a>
        <!-- دالة الـ Fetch الاستدعائية الحاقنة لستارة المنيو المنبثقة دائرياً حياً وبكفاءة عالية -->
        <button class="menu-btn-trigger" onclick="loadAndOpenSidebarMenu()"><i class="fas fa-bars"></i> القائمة</button>
    </div>

    <!-- صندوق الاستقبال الشاغر الممنوح أعلى طبقة لمنع تداخل أو تعليق كروت الواجهة -->
    <div id="dynamicMenuInjectionZone"></div>

    <div class="profile-master-container">
        
        <!-- 🦁 الغلاف الفاخر الحاوي لصورة الأسد القوطي المظلم من مجلد static وتوسيط الاسم البرمي -->
        <div class="cyber-profile-cover">
            <h2 class="cover-brand-name">ALBRAWE</h2>
        </div>
        
        <!-- 🖼️ صف الهوية البصرية والأفاتار الدائري التداخلي المبرأ من التعليق البصري -->
        <div class="profile-meta-row" id="cyberTiltAvatarZone">
            <div class="avatar-wrapper-circle" id="avatarCircleImg">
                <img class="avatar-img-circle" src="/static/avatar.png" alt="علي احمد البراوي" onerror="this.src='https://flagcdn.com'">
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
        
        <!-- 🛠️ لوحة المعلومات الموثقة لجامعة عين شمس وابن خلدون الثانوية بالملي -->
        <div class="info-dashboard-card">
            <div class="dashboard-title-row">
                <i class="fas fa-info-circle"></i> لوحة المعلومات والنبذة التعريفية المعتمدة
            </div>
            <div class="meta-info-grid">
                <div class="info-item-box">
                    <i class="fas fa-briefcase"></i>
                    <span>منشئ محتوى رقمي حياً بـ <span style="color:#fff; font-weight:bold;">Cairo</span> • عمل حر 💼</span>
                </div>
                <div class="info-item-box">
                    <i class="fas fa-graduation-cap"></i>
                    <span>درس في <span class="highlight-text-blue">Ain Shams University</span> 🎓</span>
                </div>
                <div class="info-item-box">
                    <i class="fas fa-school"></i>
                    <span>درس في <span style="color:#fff; font-weight:bold;">ابن خلدون الثانوية</span> 🏫</span>
                </div>
                <div class="info-item-box" style="border-top:1px dashed var(--border-sub); padding-top:12px; grid-column:1/-1;">
                    <i class="fas fa-user-shield" style="color:#3fb950;"></i>
                    <span><strong style="color:#fff;">نبذة برمجية:</strong> هندسة وتطوير تطبيقات الويب الكاملة باستخدام بايثون (Flask)، وتصميم الواجهات المتكاملة والمعالجات المحلية الفائقة الكفاءة لعام 2026.</span>
                </div>
            </div>
        </div>
        
    </div>

    <div class="global-footer-bar">
        حقوق النشر محفوظة برمجياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©
    </div>

    <script>
        // 🚀 محرك الـ 3D Tilt Hover التفاعلي الفاخر: حساب زوايا لمس الفأرة لإمالة صندوق الأفاتار
        const avatarBox = document.getElementById("avatarCircleImg");
        const tiltRow = document.getElementById("cyberTiltAvatarZone");

        if (window.innerWidth > 850) {
            tiltRow.addEventListener("mousemove", (e) => {
                const rect = avatarBox.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const calcX = -(y - (rect.height / 2)) / 5;
                const calcY = (x - (rect.width / 2)) / 5;
                avatarBox.style.transform = `scale(1.05) rotateX(${calcX}deg) rotateY(${calcY}deg)`;
            });
            tiltRow.addEventListener("mouseleave", () => {
                avatarBox.style.transform = "scale(1) rotateX(0deg) rotateY(0deg)";
            });
        }

        // الخوارزمية التزامنية لسحب وحقن الستارة المنبثقة دائرياً من menu.py حياً وبدون أي تعليق كلياً
        function loadAndOpenSidebarMenu() {
            const zone = document.getElementById("dynamicMenuInjectionZone");
            if (zone.innerHTML.trim() !== "") { toggleSidebarMenu(true); return; }
            
            fetch('/api/get_sidebar_menu')
            .then(res => res.json())
            .then(data => {
                const styleNode = document.createElement("style");
                styleNode.innerHTML = data.css;
                document.head.appendChild(styleNode);
                zone.innerHTML = data.html;
                setTimeout(() => { toggleSidebarMenu(true); }, 20);
            }).catch(() => { alert("❌ عطل طارئ: تعذر سحب مستودع الستارة الجانبية."); });
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

@home_blueprint.route('/')
def home_page():
    return render_template_string(HOME_HTML)
