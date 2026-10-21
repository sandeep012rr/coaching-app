import os

# Files aur unka code dictionary me store hai
project_files = {
    # 1. requirements.txt
    "requirements.txt": """Flask==3.0.0
gunicorn==21.2.0
""",

    # 2. Procfile
    "Procfile": "web: gunicorn app:app\n",

    # 3. app.py
    "app.py": '''import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "special_education_needs_secret_2026"

ADMIN_PASSWORD = "admin123"

TESTS_FILE = 'tests.json'
CONFIG_FILE = 'config.json'
COURSES_FILE = 'courses.json'
USERS_FILE = 'users.json'

def load_json(filepath, default_data):
    if not os.path.exists(filepath):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
        except Exception:
            return default_data
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default_data

def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Save Error:", e)

DEFAULT_COURSES = [
    {"id": 1, "title": "SPECIAL EDUCATION MCQ BATCH", "price": 1199, "orig_price": 2199, "discount": "45.48% off", "coupon": "", "badge": "New"},
    {"id": 2, "title": "DSSSB PRT SPECIAL EDUCATION", "price": 899, "orig_price": 1500, "discount": "Selection Batch", "coupon": "", "badge": "New"},
    {"id": 3, "title": "KVS INTERVIEW PREPARATION", "price": 899, "orig_price": 999, "discount": "10.01% off", "coupon": "", "badge": "Interview Course"},
    {"id": 4, "title": "Punjab Special Education – Primary & Master Cadre", "price": 899, "orig_price": 1200, "discount": "Special Offer", "coupon": "", "badge": "New"},
    {"id": 5, "title": "Special Education All In One", "price": 10000, "orig_price": 15000, "discount": "33.33% off", "coupon": "", "badge": "Master Pack"},
    {"id": 6, "title": "Integrated Special and Inclusive Teacher Education Programme (ISITEP)", "price": 10000, "orig_price": 15000, "discount": "33.33% off", "coupon": "", "badge": "ISITEP"},
    {"id": 7, "title": "Rajasthan 1st Grade School Lecturer (Special Education) Complete Batch 2026", "price": 1999, "orig_price": 2999, "discount": "Target Batch", "coupon": "", "badge": "Batch 2026"},
    {"id": 8, "title": "DSSSB TGT SPECIAL EDUCATION", "price": 899, "orig_price": 1500, "discount": "40.07% off", "coupon": "", "badge": "Selection Batch"}
]

DEFAULT_CONFIG = {
    "live_title": "Special Education Live Class",
    "live_url": "https://www.youtube-nocookie.com/embed/live_stream",
    "is_live": True,
    "contact_phone": "9828625119",
    "channel_code": "0029VbBrZUT6LwHeVGFnvl3Q"
}

@app.route('/')
def home():
    user = session.get('student_user')
    tests = load_json(TESTS_FILE, [])
    config = load_json(CONFIG_FILE, DEFAULT_CONFIG)
    courses = load_json(COURSES_FILE, DEFAULT_COURSES)
    return render_template('index.html', tests=tests, config=config, courses=courses, student=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        users = load_json(USERS_FILE, [])
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()

        if action == 'register':
            name = request.form.get('name', '').strip()
            if any(u.get('phone') == phone for u in users):
                return render_template('login.html', error="Yeh Mobile Number pehle se registered hai! Login karein.")
            new_user = {"name": name, "phone": phone, "password": password}
            users.append(new_user)
            save_json(USERS_FILE, users)
            session['student_user'] = new_user
            return redirect(url_for('home'))

        elif action == 'login':
            user = next((u for u in users if u.get('phone') == phone and u.get('password') == password), None)
            if user:
                session['student_user'] = user
                return redirect(url_for('home'))
            return render_template('login.html', error="Mobile Number ya Password galat hai!")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('student_user', None)
    return redirect(url_for('home'))

@app.route('/test/<int:test_id>')
def take_test(test_id):
    if not session.get('student_user'):
        return redirect(url_for('login'))
    tests = load_json(TESTS_FILE, [])
    target = next((t for t in tests if t.get('id') == test_id), None)
    if not target:
        return "Test nahi mila!", 404
    return render_template('test.html', test=target, student=session.get('student_user'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('action') == 'login':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        return render_template('admin.html', logged_in=False, error="Galat Admin Password!")

    if not session.get('is_admin'):
        return render_template('admin.html', logged_in=False)

    tests = load_json(TESTS_FILE, [])
    config = load_json(CONFIG_FILE, DEFAULT_CONFIG)
    courses = load_json(COURSES_FILE, DEFAULT_COURSES)
    users = load_json(USERS_FILE, [])

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_live':
            raw_url = request.form.get('live_url', '').strip()
            video_id = ""
            if "watch?v=" in raw_url:
                video_id = raw_url.split("watch?v=")[1].split("&")[0]
            elif "youtu.be/" in raw_url:
                video_id = raw_url.split("youtu.be/")[1].split("?")[0]
            elif "embed/" in raw_url:
                video_id = raw_url.split("embed/")[1].split("?")[0]

            config['live_url'] = f"https://www.youtube-nocookie.com/embed/{video_id}" if video_id else raw_url
            config['live_title'] = request.form.get('live_title')
            config['is_live'] = 'is_live' in request.form
            save_json(CONFIG_FILE, config)

        elif action == 'create_test':
            new_test = {
                "id": len(tests) + 1,
                "title": request.form.get('title'),
                "duration": int(request.form.get('duration', 30)),
                "questions": []
            }
            tests.append(new_test)
            save_json(TESTS_FILE, tests)

        elif action == 'add_question':
            test_id = int(request.form.get('test_id'))
            for t in tests:
                if t['id'] == test_id:
                    t['questions'].append({
                        "question": request.form.get('question'),
                        "options": [
                            request.form.get('opt_a'),
                            request.form.get('opt_b'),
                            request.form.get('opt_c'),
                            request.form.get('opt_d')
                        ],
                        "answer": request.form.get('answer').lower(),
                        "solution": request.form.get('solution', '')
                    })
                    break
            save_json(TESTS_FILE, tests)

        elif action == 'update_course':
            c_id = int(request.form.get('course_id'))
            for c in courses:
                if c['id'] == c_id:
                    c['price'] = int(request.form.get('price'))
                    c['coupon'] = request.form.get('coupon', '').strip()
                    c['discount'] = request.form.get('discount', '').strip()
                    break
            save_json(COURSES_FILE, courses)

        elif action == 'delete_test':
            t_id = int(request.form.get('test_id'))
            tests = [t for t in tests if t['id'] != t_id]
            save_json(TESTS_FILE, tests)

        return redirect(url_for('admin'))

    return render_template('admin.html', logged_in=True, tests=tests, config=config, courses=courses, total_students=len(users))

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
''',

    # 4. templates/index.html
    "templates/index.html": """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>special education needs</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f6f7fb; -webkit-tap-highlight-color: transparent; }
        .app-card { box-shadow: 0 4px 14px rgba(44, 62, 107, 0.08); border: 1.5px solid #edf2f9; transition: all 0.2s ease; }
        .app-card:active { transform: scale(0.95); background-color: #f0f4ff; }
    </style>
</head>
<body class="pb-24">
    <header class="sticky top-0 z-30 bg-white/95 backdrop-blur-md px-4 py-3 flex items-center justify-between border-b border-slate-100">
        <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-2xl text-slate-700">menu</span>
            <span class="text-base font-semibold text-slate-800 tracking-tight lowercase">special education needs</span>
        </div>
        <div class="flex items-center gap-2">
            {% if student %}
            <a href="/logout" class="text-[11px] bg-slate-100 text-slate-600 font-bold px-2.5 py-1 rounded-md border">Logout</a>
            {% else %}
            <a href="/login" class="text-xs bg-blue-600 text-white font-bold px-3 py-1 rounded-md shadow-sm">Login</a>
            {% endif %}
            <a href="/admin" class="text-xs bg-blue-50 text-blue-700 font-bold px-2 py-1 rounded-md border border-blue-200">Admin</a>
            <div class="relative">
                <span class="material-symbols-outlined text-slate-700 text-2xl">notifications</span>
                <span class="absolute -top-1 -right-1 bg-red-600 text-white text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">8</span>
            </div>
        </div>
    </header>

    <main class="max-w-lg mx-auto px-4 pt-3 space-y-4">
        <div>
            {% if student %}
            <h2 class="text-xl font-bold text-slate-900">Hello, {{ student.name }}</h2>
            {% else %}
            <h2 class="text-xl font-bold text-slate-900">Hello, Neetu Meena</h2>
            {% endif %}
            <p class="text-xs text-slate-500">Welcome to Special Education Learning Hub</p>
        </div>

        <div class="relative rounded-2xl overflow-hidden shadow-sm bg-gradient-to-r from-amber-50 via-white to-blue-50 border border-amber-200/60 p-4">
            <div class="flex items-center gap-2 mb-1">
                <span class="bg-red-600 text-white text-[10px] font-black uppercase px-2 py-0.5 rounded-full tracking-wider">Welcome</span>
                <p class="text-xs font-semibold text-amber-800">आप सभी का परिवार में स्वागत है!</p>
            </div>
            <h3 class="text-sm font-bold text-slate-900 leading-snug">SPECIAL EDUCATION NEEDS</h3>
            <p class="text-[11px] text-slate-600 mt-1 leading-normal">
                हम आपके हर कदम में साथ हैं! RPSC, DSSSB, REET और KVS Special Education भर्ती परीक्षा की सम्पूर्ण तैयारी।
            </p>
            <div class="mt-3 flex items-center justify-between pt-2 border-t border-slate-200/60 text-xs">
                <a href="tel:9828625119" class="flex items-center gap-1 font-bold text-blue-700">
                    <span class="material-symbols-outlined text-base">call</span> 9828625119
                </a>
                <a href="https://whatsapp.com/channel/0029VbBrZUT6LwHeVGFnvl3Q" target="_blank" class="flex items-center gap-1 font-bold text-emerald-600">
                    <span class="material-symbols-outlined text-base">group</span> WhatsApp Channel
                </a>
            </div>
        </div>

        {% if config.is_live %}
        <div class="bg-white rounded-2xl shadow-sm p-3.5 border border-red-100">
            <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 bg-red-600 rounded-full animate-ping"></span>
                    <span class="text-xs font-bold text-red-600 uppercase tracking-wide">Live Stream</span>
                </div>
            </div>
            <p class="text-xs font-semibold text-slate-800 mb-2 truncate">{{ config.live_title }}</p>
            <div class="relative w-full aspect-video rounded-xl overflow-hidden bg-black shadow-inner">
                <iframe class="w-full h-full" src="{{ config.live_url }}" frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
        {% endif %}

        <div class="grid grid-cols-3 gap-3 pt-1">
            <div onclick="openCoursesModal()" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mb-2 border border-blue-100">
                    <span class="material-symbols-outlined text-2xl">school</span>
                </div>
                <span class="text-xs font-medium text-slate-800">Courses</span>
            </div>
            <div onclick="openModal('MY Timetable', '• 10:00 AM: Special Act<br>• 02:00 PM: Pedagogy<br>• 08:00 PM: Mock Test')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-2 border border-indigo-100">
                    <span class="material-symbols-outlined text-2xl">calendar_month</span>
                </div>
                <span class="text-xs font-medium text-slate-800">MY Timetable</span>
            </div>
            <div onclick="openModal('Latest Update', 'RPSC 1st Grade aur DSSSB Special Educator vacancy notifications update live.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center mb-2 border border-amber-100">
                    <span class="material-symbols-outlined text-2xl">newspaper</span>
                </div>
                <span class="text-xs font-medium text-slate-800">Latest update</span>
            </div>
            <div onclick="window.scrollTo({top: 0, behavior: 'smooth'})" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-red-50 text-red-600 flex items-center justify-center mb-2 border border-red-100">
                    <span class="material-symbols-outlined text-2xl">smart_display</span>
                </div>
                <span class="text-xs font-medium text-slate-800 leading-tight">Youtube classes</span>
            </div>
            <div onclick="openModal('Notes & PDFs', 'Handwritten Notes & Special Education Material available soon.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-2 border border-rose-100">
                    <span class="material-symbols-outlined text-2xl">picture_as_pdf</span>
                </div>
                <span class="text-xs font-medium text-slate-800">Notes & PDFs</span>
            </div>
            <div onclick="scrollToTests()" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center mb-2 border border-teal-100">
                    <span class="material-symbols-outlined text-2xl">quiz</span>
                </div>
                <span class="text-xs font-semibold text-blue-900">Test Series</span>
            </div>
            <div onclick="openModal('E-Books', 'Bilingual 7000 MCQ Question Bank jald live hoga.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center mb-2 border border-purple-100">
                    <span class="material-symbols-outlined text-2xl">menu_book</span>
                </div>
                <span class="text-xs font-medium text-slate-800">E-Book</span>
            </div>
            <div onclick="scrollToTests()" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center mb-2 border border-sky-100">
                    <span class="material-symbols-outlined text-2xl">assignment_turned_in</span>
                </div>
                <span class="text-xs font-medium text-slate-800">Quiz</span>
            </div>
            <a href="tel:9828625119" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-2 border border-emerald-100">
                    <span class="material-symbols-outlined text-2xl">support_agent</span>
                </div>
                <span class="text-xs font-medium text-slate-800 leading-tight">Contact & Help</span>
            </a>
            <div onclick="openModal('Blog', 'Educational Articles & Guidelines.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-cyan-50 text-cyan-600 flex items-center justify-center mb-2 border border-cyan-100">
                    <span class="material-symbols-outlined text-2xl">article</span>
                </div>
                <span class="text-xs font-medium text-slate-800">Blog</span>
            </div>
            <div onclick="openModal('Current Affairs', 'Disability & Special Education Current Affairs 2026.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center mb-2 border border-orange-100">
                    <span class="material-symbols-outlined text-2xl">public</span>
                </div>
                <span class="text-xs font-medium text-slate-800 leading-tight">Current Affairs</span>
            </div>
            <div onclick="openModal('1 to 1 Mentorship', 'Direct counseling ke liye call karein: 9828625119')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[96px]">
                <div class="w-12 h-12 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center mb-2 border border-violet-100">
                    <span class="material-symbols-outlined text-2xl">group</span>
                </div>
                <span class="text-xs font-medium text-slate-800 leading-tight">1 to 1 section</span>
            </div>
        </div>

        <div id="test-series-anchor" class="pt-2">
            <h3 class="text-base font-bold text-slate-800 mb-3 flex items-center gap-1.5">
                <span class="material-symbols-outlined text-blue-700">fact_check</span> Active Test Series
            </h3>
            <div class="space-y-2.5">
                {% for test in tests %}
                <div class="bg-white rounded-xl p-3.5 border border-slate-200/80 shadow-sm flex items-center justify-between">
                    <div>
                        <h4 class="text-sm font-bold text-slate-900">{{ test.title }}</h4>
                        <p class="text-xs text-slate-500 mt-1">⏱️ {{ test.duration }} Min | {{ test.questions|length }} Sawal</p>
                    </div>
                    <a href="/test/{{ test.id }}" class="bg-blue-600 text-white text-xs font-bold px-4 py-2 rounded-lg">Start Test</a>
                </div>
                {% else %}
                <div class="bg-white p-6 rounded-xl text-center text-xs text-slate-400 border border-dashed border-slate-200">
                    Abhi koi test live nahi hai. Admin panel se test add karein.
                </div>
                {% endfor %}
            </div>
        </div>
    </main>

    <div id="courses-modal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm hidden flex items-end sm:items-center justify-center">
        <div class="bg-white rounded-t-3xl sm:rounded-2xl max-w-lg w-full max-h-[88vh] flex flex-col shadow-2xl overflow-hidden">
            <div class="p-4 border-b flex items-center justify-between bg-slate-50">
                <h3 class="font-bold text-slate-800 text-base">All Special Education Courses</h3>
                <button onclick="closeCoursesModal()" class="w-8 h-8 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center">✕</button>
            </div>
            <div class="p-4 overflow-y-auto space-y-3.5">
                {% for c in courses %}
                <div class="border rounded-xl p-3.5 bg-white shadow-sm flex flex-col gap-2">
                    <div class="flex items-start justify-between">
                        <div>
                            <span class="bg-amber-100 text-amber-800 text-[10px] font-bold px-2 py-0.5 rounded">{{ c.badge }}</span>
                            <h4 class="font-bold text-slate-900 text-sm mt-1">{{ c.title }}</h4>
                        </div>
                        <span class="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">{{ c.discount }}</span>
                    </div>
                    <div class="flex items-center justify-between pt-1">
                        <span class="text-base font-extrabold text-slate-900">₹ {{ c.price }}</span>
                        <a href="https://wa.me/919828625119?text=Mujhe%20{{ c.title }}%20chahiye" target="_blank" class="bg-blue-600 text-white text-xs font-bold px-4 py-1.5 rounded-lg">Join Now</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <div id="info-modal" class="fixed inset-0 z-50 bg-black/50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-sm w-full p-5 shadow-2xl space-y-3">
            <h4 id="modal-title" class="font-bold text-slate-800 text-base"></h4>
            <div id="modal-body" class="text-xs text-slate-600 space-y-2"></div>
            <button onclick="closeModal()" class="w-full bg-blue-600 text-white text-xs font-bold py-2.5 rounded-xl">Close</button>
        </div>
    </div>

    <script>
        function openCoursesModal() { document.getElementById('courses-modal').classList.remove('hidden'); }
        function closeCoursesModal() { document.getElementById('courses-modal').classList.add('hidden'); }
        function scrollToTests() { document.getElementById('test-series-anchor').scrollIntoView({ behavior: 'smooth' }); }
        function openModal(t, b) {
            document.getElementById('modal-title').innerText = t;
            document.getElementById('modal-body').innerHTML = b;
            document.getElementById('info-modal').classList.remove('hidden');
        }
        function closeModal() { document.getElementById('info-modal').classList.add('hidden'); }
    </script>
</body>
</html>
""",

    # 5. templates/admin.html
    "templates/admin.html": """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Control Panel</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
</head>
<body class="bg-slate-100 min-h-screen text-slate-800 font-sans pb-16">
    {% if not logged_in %}
    <div class="flex items-center justify-center min-h-screen p-4">
        <div class="bg-white rounded-2xl shadow-xl max-w-sm w-full p-6 text-center space-y-4 border">
            <h2 class="text-xl font-bold">Admin Login</h2>
            {% if error %}<p class="text-red-600 text-xs font-bold">{{ error }}</p>{% endif %}
            <form method="POST" class="space-y-3">
                <input type="hidden" name="action" value="login">
                <input type="password" name="password" placeholder="Password (admin123)" class="w-full border rounded-xl p-3 text-sm" required>
                <button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-xl text-sm">Login</button>
            </form>
            <a href="/" class="text-xs text-slate-400 block">&larr; Back to App</a>
        </div>
    </div>
    {% else %}
    <header class="bg-blue-900 text-white px-6 py-4 flex justify-between items-center shadow">
        <h1 class="font-bold">Admin Panel</h1>
        <div>
            <a href="/" target="_blank" class="bg-blue-800 text-xs px-3 py-1.5 rounded mr-2">View App</a>
            <a href="/admin/logout" class="bg-red-600 text-xs px-3 py-1.5 rounded">Logout</a>
        </div>
    </header>

    <main class="max-w-3xl mx-auto p-4 space-y-6">
        <div class="bg-white p-5 rounded-2xl shadow-sm border">
            <h2 class="font-bold text-red-600 mb-3">Live Class YouTube Link</h2>
            <form method="POST" class="space-y-3 text-xs">
                <input type="hidden" name="action" value="update_live">
                <input type="text" name="live_title" value="{{ config.live_title }}" placeholder="Topic" class="w-full border p-2 rounded" required>
                <input type="text" name="live_url" value="{{ config.live_url }}" placeholder="YouTube Link" class="w-full border p-2 rounded" required>
                <label class="flex items-center gap-2">
                    <input type="checkbox" name="is_live" {% if config.is_live %}checked{% endif %}> Live Show Karein
                </label>
                <button type="submit" class="bg-red-600 text-white font-bold px-4 py-2 rounded">Save Live Class</button>
            </form>
        </div>

        <div class="bg-white p-5 rounded-2xl shadow-sm border">
            <h2 class="font-bold text-green-700 mb-3">Naya Test Banayein</h2>
            <form method="POST" class="flex gap-2 text-xs">
                <input type="hidden" name="action" value="create_test">
                <input type="text" name="title" placeholder="Test Name" class="w-2/3 border p-2 rounded" required>
                <input type="number" name="duration" value="30" placeholder="Min" class="w-1/3 border p-2 rounded" required>
                <button type="submit" class="bg-green-600 text-white font-bold px-4 py-2 rounded">Add</button>
            </form>
        </div>

        <div class="bg-white p-5 rounded-2xl shadow-sm border">
            <h2 class="font-bold text-blue-800 mb-3">Test me Sawal Jodein</h2>
            <form method="POST" class="space-y-3 text-xs">
                <input type="hidden" name="action" value="add_question">
                <select name="test_id" class="w-full border p-2 rounded" required>
                    {% for t in tests %}
                    <option value="{{ t.id }}">{{ t.title }}</option>
                    {% endfor %}
                </select>
                <textarea name="question" placeholder="Question text..." class="w-full border p-2 rounded" required></textarea>
                <div class="grid grid-cols-2 gap-2">
                    <input type="text" name="opt_a" placeholder="Option A" class="border p-2 rounded" required>
                    <input type="text" name="opt_b" placeholder="Option B" class="border p-2 rounded" required>
                    <input type="text" name="opt_c" placeholder="Option C" class="border p-2 rounded" required>
                    <input type="text" name="opt_d" placeholder="Option D" class="border p-2 rounded" required>
                </div>
                <div class="flex gap-2">
                    <select name="answer" class="border p-2 rounded uppercase w-1/3" required>
                        <option value="a">A</option><option value="b">B</option><option value="c">C</option><option value="d">D</option>
                    </select>
                    <input type="text" name="solution" placeholder="Explanation" class="border p-2 rounded w-2/3">
                </div>
                <button type="submit" class="bg-blue-700 text-white font-bold px-4 py-2 rounded">Sawal Save Karein</button>
            </form>
        </div>
    </main>
    {% endif %}
</body>
</html>
""",

    # 6. templates/login.html
    "templates/login.html": """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Student Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
    <style>body { font-family: 'Inter', sans-serif; background-color: #f6f7fb; }</style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="bg-white rounded-3xl shadow-xl max-w-sm w-full p-6 space-y-5 border border-slate-100">
        <div class="text-center space-y-1">
            <span class="material-symbols-outlined text-4xl text-blue-700">school</span>
            <h2 class="text-xl font-bold text-slate-900">Student Portal</h2>
            <p class="text-xs text-slate-500">special education needs</p>
        </div>
        {% if error %}
        <div class="bg-red-50 text-red-600 text-xs p-2.5 rounded-xl font-semibold text-center border border-red-100">
            {{ error }}
        </div>
        {% endif %}
        <div class="flex bg-slate-100 p-1 rounded-xl text-xs font-bold text-slate-600">
            <button id="tab-login" onclick="showTab('login')" class="w-1/2 py-2 rounded-lg bg-white text-blue-700 shadow-sm">Login</button>
            <button id="tab-register" onclick="showTab('register')" class="w-1/2 py-2 rounded-lg text-slate-500">Register</button>
        </div>
        <form id="form-login" method="POST" class="space-y-3">
            <input type="hidden" name="action" value="login">
            <input type="tel" name="phone" placeholder="Mobile Number" class="w-full border rounded-xl p-3 text-xs" required>
            <input type="password" name="password" placeholder="Password" class="w-full border rounded-xl p-3 text-xs" required>
            <button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-xl text-xs">Sign In</button>
        </form>
        <form id="form-register" method="POST" class="space-y-3 hidden">
            <input type="hidden" name="action" value="register">
            <input type="text" name="name" placeholder="Full Name" class="w-full border rounded-xl p-3 text-xs" required>
            <input type="tel" name="phone" placeholder="Mobile Number" class="w-full border rounded-xl p-3 text-xs" required>
            <input type="password" name="password" placeholder="Password" class="w-full border rounded-xl p-3 text-xs" required>
            <button type="submit" class="w-full bg-emerald-600 text-white font-bold py-3 rounded-xl text-xs">Register</button>
        </form>
        <a href="/" class="text-xs text-center block text-slate-400">&larr; Back to Home</a>
    </div>
    <script>
        function showTab(t) {
            const l = document.getElementById('form-login'), r = document.getElementById('form-register');
            const tl = document.getElementById('tab-login'), tr = document.getElementById('tab-register');
            if (t === 'login') {
                l.classList.remove('hidden'); r.classList.add('hidden');
                tl.className = "w-1/2 py-2 rounded-lg bg-white text-blue-700 shadow-sm";
                tr.className = "w-1/2 py-2 rounded-lg text-slate-500";
            } else {
                l.classList.add('hidden'); r.classList.remove('hidden');
                tr.className = "w-1/2 py-2 rounded-lg bg-white text-emerald-700 shadow-sm";
                tl.className = "w-1/2 py-2 rounded-lg text-slate-500";
            }
        }
    </script>
</body>
</html>
""",

    # 7. templates/test.html
    "templates/test.html": """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ test.title }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 p-4">
    <div class="max-w-xl mx-auto bg-white p-5 rounded-2xl shadow">
        <h2 class="text-lg font-bold text-blue-900 mb-2">{{ test.title }}</h2>
        <p class="text-xs text-slate-500 mb-4">⏱️ Duration: {{ test.duration }} Minutes</p>
        <div id="quiz-box">
            {% for q in test.questions %}
            <div class="mb-4 p-3 border rounded-lg">
                <p class="font-semibold text-sm">Q{{ loop.index }}. {{ q.question }}</p>
                <div class="mt-2 space-y-1 text-xs">
                    {% for opt in q.options %}
                    <label class="block p-2 border rounded cursor-pointer hover:bg-slate-50">
                        <input type="radio" name="q{{ loop.index0 }}" value="{{ ['a','b','c','d'][loop.index0] }}"> {{ opt }}
                    </label>
                    {% endfor %}
                </div>
            </div>
            {% else %}
            <p class="text-xs text-slate-400">Is test me abhi koi sawal nahi hai.</p>
            {% endfor %}
        </div>
        <a href="/" class="inline-block mt-3 bg-blue-600 text-white text-xs font-bold px-4 py-2 rounded-lg">Back to Home</a>
    </div>
</body>
</html>
"""
}

# Auto folder and file creator
for path, content in project_files.items():
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"File created successfully: {path}")

print("\nAll folders and files have been generated perfectly!")
