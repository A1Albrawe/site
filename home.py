from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

# عزل التنسيقات الكونية المتجاوبة لحماية النواة والـ CSS من التعارض النصي للأقواس خارج الصندوق
HOME_CSS = """
<style>
    :root {
        --bg-global: #030508; --text-main: #c9d1d9; --bg-card: rgba(13, 17, 23, 0.75); 
        --border-main: #21262d; --border-neon: #3fb950; --border-cyber: #ff007f; --text-white: #fff; --border-sub: #30363d;
    }
    
    body { font-family: 'Courier New', Courier, monospace; background: var(--bg-global); color: var(--text-main); margin: 0; padding: 25px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; overflow-x: hidden; position: relative; }
    
    /* 🪐 هندسة ومحرك مصفوفة الرادار الكوني التكتيكي الخلفي المتحرك (Dynamic Cosmic Radar Canvas) */
    .radar-background-grid { position: fixed; top: 50%; left: 50%; width: 140vw; height: 140vw; transform: translate(-50%, -50%); border-radius: 50%; border: 1px solid rgba(63, 185, 80, 0.15); pointer-events: none; z-index: 1; animation: radarRotate 25s linear infinite; display: flex; align-items: center; justify-content: center; }
    .radar-background-grid::before { content: ''; position: absolute; width: 70%; height: 70%; border-radius: 50%; border: 1px dashed rgba(255, 0, 127, 0.12); animation: radarPulse 4s ease-in-out infinite alternate; }
    .radar-background-grid::after { content: ''; position: absolute; width: 40%; height: 40%; border-radius: 50%; border: 2px solid rgba(88, 166, 255, 0.08); }
    .radar-sweep-line { position: absolute; top: 50%; left: 50%; width: 50%; height: 2px; background: linear-gradient(90deg, rgba(63,185,80,0.4) 0%, rgba(63,185,80,0) 100%); transform-origin: left center; animation: sweepSweep 6s linear infinite; }

    @keyframes radarRotate { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
    @keyframes radarPulse { 0% { transform: scale(0.9); opacity: 0.3; } 100% { transform: scale(1.1); opacity: 1; } }
    @keyframes sweepSweep { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    /* 🌐 شريط الهيدر العلوي الموحد الثابت */
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1200px; margin: 0 auto 35px auto; border-bottom: 2px solid var(--border-sub); padding-bottom: 14px; box-sizing: border-box; position: relative; z-index: 100; }
    .brand-logo { font-size: 24px; font-weight: bold; color: var(--text-white); text-shadow: 0 0 10px var(--border-neon), 0 0 20px var(--border-cyber); text-decoration: none; font-family: monospace; cursor: pointer; }
    .menu-btn-trigger { background: #161b22; border: 1px solid var(--border-sub); color: var(--border-neon); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 6px; font-family: inherit; transition: 0.2s; box-shadow: 0 0 10px rgba(63,185,80,0.1); }
    .menu-btn-trigger:hover { background: var(--border-neon); color: #000; box-shadow: 0 0 15px var(--border-neon); }
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; position: relative; z-index: 10; }
    
    /* 💻 كرت العرض ثنائي الأجنحة المطور والمحمي بـ محرك تحريك تفاعلي 3D ليميل ويتوهج مع الحركة حياً */
    .responsive-profile-wrapper { 
        display: flex; flex-direction: row; gap: 40px; width: 100%; max-width: 1100px; 
        background: var(--bg-card); border: 1px solid var(--border-main); border-radius: 20px; 
        padding: 45px; box-shadow: 0 35px 70px rgba(0,0,0,0.7); 
        border-bottom: 4px solid var(--border-neon); border-right: 4px solid var(--border-cyber);
        box-sizing: border-box; align-items: center; direction: rtl; 
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        
        /* تفعيل عمق الأبعاد الثلاثية لـ بايثون والجافا سكريبت */
        transform-style: preserve-3d;
        transform: perspective(1000px) rotateX(0deg) rotateY(0deg);
        transition: transform 0.15s ease, box-shadow 0.3s ease;
    }
    .responsive-profile-wrapper:hover {
        box-shadow: 0 0 30px rgba(63,185,80,0.15), 0 0 40px rgba(255,0,127,0.15);
    }
    
    .profile-sidebar-zone { flex: 1; max-width: 280px; display: flex; flex-direction: column; align-items: center; text-align: center; border-left: 2px solid var(--border-sub); padding-left: 30px; box-sizing: border-box; transform: translateZ(30px); }
    .profile-content-zone { flex: 2; display: flex; flex-direction: column; justify-content: center; text-align: right; box-sizing: border-box; padding-right: 10px; transform: translateZ(20px); }
    
    .avatar-wrapper { width: 150px; height: 150px; border-radius: 18px; border: 2px solid var(--border-cyber); overflow: hidden; box-shadow: 0 0 25px rgba(255,0,127,0.25); margin-bottom: 20px; display: flex; align-items: center; justify-content: center; background: #04060a; }
    .avatar-img { width: 100%; height: 100%; object-fit: cover; display: block; }
    
    .profile-name { font-size: 30px; font-weight: bold; color: var(--text-white); margin: 0 0 8px 0; text-shadow: 0 0 8px rgba(255,255,255,0.2); font-family: monospace; }
    .profile-title { font-size: 11.5px; font-weight: bold; color: var(--border-neon); margin: 0; text-transform: uppercase; letter-spacing: 0.8px; text-shadow: 0 0 6px rgba(63,185,80,0.3); }
    
    .details-sub-box { display: flex; flex-direction: column; gap: 16px; font-size: 15px; line-height: 1.7; }
    .meta-item { display: block; color: var(--text-main); }
    .meta-label { font-weight: bold; color: var(--text-white); text-shadow: 0 0 4px rgba(255,255,255,0.1); }
    .tech-highlight { color: #58a6ff; font-weight: bold; font-family: monospace; text-shadow: 0 0 6px rgba(88,166,255,0.2); }
    
    .global-footer-bar { width: 100%; text-align: center; margin-top: 40px; padding-top: 15px; border-top: 1px solid var(--border-sub); font-size: 12px; color: #8b949e; font-family: monospace; position: relative; z-index: 100; }
    
    @media (max-width: 850px) {
        body { padding: 15px; } .top-nav { max-width: 100%; } .responsive-profile-wrapper { flex-direction: column; align-items: center; padding: 25px; max-width: 440px; transform: none !important; }
        .profile-sidebar-zone { flex: none; width: 100%; max-width: 100%; border-left: none; border-bottom: 2px solid var(--border-sub); padding-left: 0; padding-bottom: 25px; margin-bottom: 20px; }
        .profile-content-zone { width: 100%; padding-right: 0; }
    }
</style>
"""
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe | البوابة الرسمية الموحدة لعام 2026</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="shortcut icon" type="image/x-icon" href="/static/favicon.ico">
    """ + HOME_CSS + """
</head>
<body>

    <!-- 🪐 حقن وحياكة كتل رادار الفضاء العسكري الخلفي الدائم الحركة -->
    <div class="radar-background-grid">
        <div class="radar-sweep-line"></div>
    </div>

    <div class="top-nav">
        <!-- النقر على الشعار يعيد التوجيه فوراً لمسار الجذر صيانة للروابط الشاملة -->
        <a href="/" class="brand-logo">Albrawe</a>
        <!-- دالة الـ Fetch الاستدعائية الحاقنة لستارة المنيو المنبثقة دائرياً حياً -->
        <button class="menu-btn-trigger" onclick="loadAndOpenSidebarMenu()"><i class="fas fa-bars"></i> القائمة</button>
    </div>

    <!-- صندوق الاستقبال الشاغر لحقن كود الـ Sidebar المطور المنبثق دائرياً من menu.py حياً -->
    <div id="dynamicMenuInjectionZone"></div>

    <div class="main-container">
        <!-- 💻 كرت العرض التفاعلي ثنائي الأجنحة المحمي بحركات الأبعاد الثلاثية لراحة زوارك -->
        <div class="responsive-profile-wrapper" id="cyberTiltCard3D">
            
            <!-- جناح الهوية البرمجية وشعار الهكر المضيء -->
            <div class="profile-sidebar-zone">
                <div class="avatar-wrapper">
                    <!-- جلب الصورة الصافية المعتمدة وتخطي أي حجب سحابي من الجذر -->
                    <img class="avatar-img" src="/static/avatar.png" alt="Albrawe Profile" onerror="this.src='https://flagcdn.com'">
                </div>
                <h1 class="profile-name">Albrawe</h1>
                <div class="profile-title">Architecture & Software Engineer</div>
            </div>
            
            <!-- جناح النبذة والخبرات والتقنيات التكتيكية بالملي -->
            <div class="profile-content-zone">
                <div class="details-sub-box">
                    <span class="meta-item">
                        ⚡ <span class="meta-label">خبراتي:</span> بناء وتطوير تطبيقات الويب الكاملة، وتصميم وتعديل اسكريبتات البايثون. إنشاء وتصميم صفحات الويب المتكاملة، معالجة البيانات المحلية، والواجهات الذكية.
                    </span>
                    <span class="meta-item" style="border-top: 1px dashed var(--border-sub); padding-top: 12px; margin-top: 2px;">
                        🛠️ <span class="meta-label">التقنيات الأساسية:</span>
                        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                            <div>🔹 <span class="tech-highlight">Python (Flask)</span></div>
                            <div>🔹 <span class="tech-highlight">JavaScript (ES6)</span></div>
                        </div>
                    </span>
                </div>
            </div>
            
        </div>
    </div>

    <!-- ذيل حقوق النشر الثابت المعزز لجميع الواجهات -->
    <div class="global-footer-bar">
        حقوق النشر محفوظة برمجياً وتعود إلى المسؤول البراوي بتاريخ 2026 ©
    </div>
"""
    <!-- 🚀 محرك جافا سكريبت المزامنة وحساب زوايا الميل والالتفاف ثلاثي الأبعاد حياً بالبكسل -->
    <script>
        const card3D = document.getElementById("cyberTiltCard3D");

        // حساب حركة الفأرة ولمس الشاشة لـ لف وإمالة الكرت بزوايا حادة نيونية
        if (window.innerWidth > 850) {
            card3D.addEventListener("mousemove", (e) => {
                const rect = card3D.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const calcX = -(y - (rect.height / 2)) / 14;
                const calcY = (x - (rect.width / 2)) / 22;
                
                card3D.style.transform = `perspective(1000px) rotateX(${calcX}deg) rotateY(${calcY}deg)`;
            });
            
            card3D.addEventListener("mouseleave", () => {
                card3D.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg)";
            });
        }

        // الخوارزمية التزامنية لسحب الستارة المنبثقة دائرياً من menu.py وحقنها حياً فورا
        function loadAndOpenSidebarMenu() {
            const zone = document.getElementById("dynamicMenuInjectionZone");
            
            if (zone.innerHTML.trim() !== "") {
                toggleSidebarMenu(true);
                return;
            }
            
            fetch('/api/get_sidebar_menu')
            .then(res => res.json())
            .then(data => {
                const styleNode = document.createElement("style");
                styleNode.innerHTML = data.css;
                document.head.appendChild(styleNode);
                
                zone.innerHTML = data.html;
                setTimeout(() => { toggleSidebarMenu(true); }, 20);
            }).catch(() => { alert("❌ عطل طارئ: تعذر جلب مستودع الستارة الدائرية المنبثقة."); });
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
            if (panel.style.display === "flex") {
                panel.style.display = "none";
                trigger.classList.remove("open-state");
            } else {
                panel.style.display = "flex";
                trigger.classList.add("open-state");
            }
        }
    </script>
</body>
</html>
"""

@home_blueprint.route('/')
def home_page():
    return render_template_string(HOME_HTML)
