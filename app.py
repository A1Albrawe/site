from flask import Flask, request, session, redirect, render_template_string

app = Flask(__name__)
app.secret_key = "ALBRAWE_FINAL_CORE_LOCK_2026"

# 🛡️ خوارزمية الاستدعاء المعزول كلياً سيبرانياً لحماية الحاوية المشتركة من التعارض
try:
    from home import home_blueprint
    app.register_blueprint(home_blueprint)
except Exception: pass

try:
    from menu import menu_blueprint
    app.register_blueprint(menu_blueprint)
except Exception: pass

try:
    from admin import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/albrawe-admin-panel-2026')
except Exception: pass

try:
    from api import api_blueprint
    app.register_blueprint(api_blueprint)
except Exception: pass

try:
    from report import report_blueprint
    app.register_blueprint(report_blueprint)
except Exception: pass

try:
    from about import about_blueprint
    app.register_blueprint(about_blueprint)
except Exception: pass

try:
    from projects import projects_blueprint
    app.register_blueprint(projects_blueprint)
except Exception: pass

try:
    from scripts import scripts_blueprint
    app.register_blueprint(scripts_blueprint)
except Exception: pass

# الاستدعاء الموحد لملفات باقة الألعاب الستة المتواجدة بداخل مجلد games_package
try: from games_package.snake import snake_blueprint
except Exception: pass
try: from games_package.tetris import tetris_blueprint
except Exception: pass
try: from games_package.xo import xo_blueprint
except Exception: pass
try: from games_package.shooter import shooter_blueprint
except Exception: pass
try: from games_package.clicker import clicker_blueprint
except Exception: pass
try: from games_package.card_game import card_game_blueprint
except Exception: pass
@app.after_request
def inject_global_analytics_tracker(response):
    """
    مُحرك الرصد والمزامنة العالمي!
    تم تنظيف صياغته وحظر رصد ملفات الصور والـ Favicon واللوحة لمنع ومسح الـ 500 كلياً،
    مع المحافظة الكاملة على تجميع وتمرير ثواني استخدام باقة الألعاب حياً.
    """
    if request.path.endswith('.ico') or request.path.endswith('.png') or request.path.endswith('.jpg'):
        return response

    if response.content_type and response.content_type.startswith('text/html'):
        try:
            if "albrawe-admin-panel-2026" in request.path or "albrawe-admin" in request.path:
                return response
                
            text = response.get_data(as_text=True)
            
            global_tracker_script = """
            <script>
                document.addEventListener("DOMContentLoaded", () => {
                    let storedUser = localStorage.getItem("albrawe_tracker_username");
                    if(!storedUser) {
                        storedUser = "لاعب_مستمر_" + Math.floor(100 + Math.random() * 900);
                        localStorage.setItem("albrawe_tracker_username", storedUser);
                    }
                    
                    let userLocation = "القاهرة - مصر 🇪🇬";
                    fetch("https://ipapi.co")
                    .then(res => res.json())
                    .then(geo => {
                        if(geo.city && geo.region && geo.country_name) {
                            userLocation = geo.city + "، " + geo.region + " - " + geo.country_name;
                        } else if(geo.city && geo.country_name) {
                            userLocation = geo.city + " - " + geo.country_name;
                        }
                        sendPayloadToServer();
                    }).catch(() => { sendPayloadToServer(); });

                    function sendPayloadToServer() {
                        fetch("/api/log_visit", {
                            method: "POST",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({ username: storedUser, location: userLocation })
                        });
                    }
                    
                    let currentPath = window.location.pathname.replace("/", "") || "site";
                    let localDuration = 0;
                    
                    setInterval(() => {
                        if (typeof isPaused !== "undefined" && isPaused) return;
                        if (typeof isGameOver !== "undefined" && isGameOver) return;
                        localDuration += 5;
                    }, 5000);
                    
                    window.addEventListener("beforeunload", () => {
                        if (localDuration > 0) {
                            navigator.sendBeacon("/api/update_duration", JSON.stringify({ 
                                username: storedUser, 
                                game: currentPath,
                                durationIncrement: localDuration
                            }));
                        }
                    });
                });
            </script>
            <script defer src="/_vercel/insights/script.js"></script>
            """
            if "</body>" in text:
                text = text.replace("</body>", global_tracker_script + "</body>")
            response.set_data(text)
        except Exception: pass
    return response

if __name__ == '__main__':
    app.run(debug=True)
