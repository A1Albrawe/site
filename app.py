import os
from flask import Flask, session

# تهيئة نواة الخادم المركزي المحصن لعام 2026
app = Flask(__name__)
app.secret_key = "albrawe_cyber_terminal_key_2026_secure"

# 🛡️ استدعاء الموديلات والواجهات البرمية القياسية المحدثة بعد حذف menu القديم كلياً
from api import api_blueprint
from home import home_blueprint
from projects import projects_blueprint
from scripts import scripts_blueprint
from report import report_blueprint
from about import about_blueprint
from admin import admin_blueprint

# تسجيل المسارات الحصينة داخل نواة الخادم
app.register_blueprint(api_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(projects_blueprint)
app.register_blueprint(scripts_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(about_blueprint)

# حقن لوحة التحليلات والرقابة السيبرانية V3 في مسار مستقل معزول
app.register_blueprint(admin_blueprint, url_prefix='/albrawe-admin-panel-2026')
@app.before_request
def guarantee_user_identity_session():
    # خوارزمية توليد بصمة الهوية الفرعية الموحدة للزوار تلقائياً فور الإقلاع
    if 'cyber_user_id' not in session:
        import random, string
        generated_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
        session['cyber_user_id'] = f"user_{generated_suffix}"

# نقطة الإقلاع والربط الأساسية المتوافقة حياً مع خوادم Vercel Serverless
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
