import datetime
from flask import Blueprint, request, jsonify

api_blueprint = Blueprint('api', __name__)

# 🛡️ تأمين الأرشيف التراكمي في بيئة خوادم Vercel Serverless ومنع تصفير السجلات
if not hasattr(api_blueprint, 'CENTRAL_ANALYTICS_SERVER_DB'):
    api_blueprint.CENTRAL_ANALYTICS_SERVER_DB = []

if not hasattr(api_blueprint, 'TOTAL_HISTORICAL_VISITS_COUNT'):
    api_blueprint.TOTAL_HISTORICAL_VISITS_COUNT = 0

if not hasattr(api_blueprint, 'PERMANENT_COMPLAINTS_SERVER_DB'):
    api_blueprint.PERMANENT_COMPLAINTS_SERVER_DB = []

@api_blueprint.route('/api/log_visit', methods=['POST'])
def log_visit():
    data = request.get_json() or {}
    username = data.get('username', 'زائر مجهول').strip()
    user_agent = request.headers.get('User-Agent', 'غير معروف')
    location = data.get('location', 'جاري جلب الموقع...').strip()
    
    # محرك الرصد والفرز السيبراني الدقيق لموديلات وماركات هواتف وأجهزة الزوار حياً
    device_model = "كمبيوتر / غير معروف"
    ua_lower = user_agent.lower()
    if "android" in ua_lower:
        device_model = "Android Device 📱"
        if "samsung" in ua_lower or "sm-" in ua_lower: device_model = "Samsung Galaxy 📱"
        elif "redmi" in ua_lower or "xiaomi" in ua_lower or "mi " in ua_lower: device_model = "Xiaomi / Redmi 📱"
        elif "oppo" in ua_lower: device_model = "Oppo Phone 📱"
        elif "huawei" in ua_lower: device_model = "Huawei Phone 📱"
    elif "iphone" in ua_lower or "ipad" in ua_lower:
        device_model = "iPhone 🍏"
    elif "windows" in ua_lower: 
        device_model = "Windows PC 💻"
    elif "macintosh" in ua_lower:
        device_model = "MacBook 💻"

    user_entry = next((item for item in api_blueprint.CENTRAL_ANALYTICS_SERVER_DB if item["username"] == username), None)
    
    if not user_entry:
        api_blueprint.TOTAL_HISTORICAL_VISITS_COUNT += 1  
        user_entry = {
            "username": username, "deviceModel": device_model, "location": location,
            "loginTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": 0, "snakeTime": 0, "tetrisTime": 0, "xoTime": 0, "shooterTime": 0, "clickerTime": 0, "cardTime": 0,
            "browsingHistory": ["الرئيسية 🏠"]
        }
        api_blueprint.CENTRAL_ANALYTICS_SERVER_DB.append(user_entry)
    else:
        user_entry["location"] = location
        user_entry["deviceModel"] = device_model
        
    return jsonify({"status": "success"})
@api_blueprint.route('/api/update_duration', methods=['POST'])
def update_duration():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    game_type = data.get('game', '')
    inc = data.get('durationIncrement', 5)
    
    if username:
        user_entry = next((item for item in api_blueprint.CENTRAL_ANALYTICS_SERVER_DB if item["username"] == username), None)
        if user_entry:
            if game_type == 'snake': user_entry["snakeTime"] += inc
            elif game_type == 'tetris': user_entry["tetrisTime"] += inc
            elif game_type == 'xo': user_entry["xoTime"] += inc
            elif game_type == 'shooter': user_entry["shooterTime"] += inc
            elif game_type == 'clicker': user_entry["clickerTime"] += inc
            elif game_type == 'card_game': user_entry["cardTime"] += inc
            else: user_entry["duration"] += inc
            
    return jsonify({"status": "success"})

@api_blueprint.route('/api/submit_complaint', methods=['POST'])
def submit_complaint():
    data = request.get_json() or {}
    user = data.get('user', 'زائر مجهول').strip()
    details = data.get('details', '').strip()
    if details:
        complaint_entry = {
            "user": user, "details": details,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        api_blueprint.PERMANENT_COMPLAINTS_SERVER_DB.append(complaint_entry)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@api_blueprint.route('/api/admin_get_all_data', methods=['GET'])
def admin_get_all_data():
    return jsonify({
        "analytics": api_blueprint.CENTRAL_ANALYTICS_SERVER_DB,
        "reports": api_blueprint.PERMANENT_COMPLAINTS_SERVER_DB,
        "historicalVisits": api_blueprint.TOTAL_HISTORICAL_VISITS_COUNT
    })

@api_blueprint.route('/api/admin_clear_data', methods=['POST'])
def admin_clear_data():
    api_blueprint.CENTRAL_ANALYTICS_SERVER_DB = []
    api_blueprint.PERMANENT_COMPLAINTS_SERVER_DB = []
    return jsonify({"status": "cleared"})
