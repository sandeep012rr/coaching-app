import os

project_files = {
    # 1. requirements.txt
    "requirements.txt": """Flask==3.0.0
gunicorn==21.2.0
""",

    # 2. Procfile
    "Procfile": "web: gunicorn app:app\n",

    # 3. app.py (With Image Slider Engine)
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
    "channel_code": "0029VbBrZUT6LwHeVGFnvl3Q",
    "slider_images": [
        "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800&auto=format&fit=crop"
    ]
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
                return render_template('login.html', error="Mobile Number pehle se registered hai! Login karein.")
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

        if action == 'add_slider_img':
            img_url = request.form.get('img_url', '').strip()
            if img_url:
                if 'slider_images' not in config:
                    config['slider_images'] = []
                if len(config['slider_images']) < 10:
                    config['slider_images'].append(img_url)
                    save_json(CONFIG_FILE, config)

        elif action == 'delete_slider_img':
            img_index = int(request.form.get('img_index'))
            if 'slider_images' in config and 0 <= img_index < len(config['slider_images']):
                config['slider_images'].pop(img_index)
                save_json(CONFIG_FILE, config)

        elif action == 'update_live':
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

    # 4. templates/admin.html (With Slider Box)
    "templates/admin.html": """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Master Admin Control Panel</title>
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
                <input type="password" name="password" placeholder="Password (admin123)" class="w-full border rounded-xl p-3 text-sm focus:outline-blue-600" required>
                <button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-xl text-sm">Login</button>
            </form>
            <a href="/" class="text-xs text-slate-400 block">&larr; Back to App</a>
        </div>
    </div>
    {% else %}
    <header class="bg-blue-900 text-white px-6 py-4 flex justify-between items-center shadow sticky top-0 z-20">
        <div>
            <h1 class="font-bold text-base">Admin Master Control</h1>
            <p class="text-[10px] text-blue-200">Registered Students: {{ total_students }}</p>
        </div>
        <div class="flex items-center gap-2">
            <a href="/" target="_blank" class="bg-blue-800 text-xs px-3 py-1.5 rounded">View App</a>
            <a href="/admin/logout" class="bg-red-600 text-xs px-3 py-1.5 rounded">Logout</a>
        </div>
    </header>

    <main class="max-w-3xl mx-auto p-4 space-y-6">

        <!-- 1. SLIDER IMAGES MANAGER -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
            <div class="flex items-center justify-between mb-3">
                <h2 class="font-bold text-amber-700 flex items-center gap-1.5 text-base">
                    <span class="material-symbols-outlined">view_carousel</span> Banner Slider Images Manager
                </h2>
                <span class="text-xs font-bold text-slate-500">Total: {{ config.slider_images|length }}/10</span>
            </div>

            <form method="POST" class="flex gap-2 mb-4">
                <input type="hidden" name="action" value="add_slider_img">
                <input type="url" name="img_url" placeholder="Image direct URL paste karein (https://...)" class="flex-grow border rounded-lg p-2 text-xs focus:outline-amber-600" required>
                <button type="submit" class="bg-amber-600 hover:bg-amber-700 text-white font-bold px-4 py-2 rounded-lg text-xs">
                    + Add Slide
                </button>
            </form>

            <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {% for img in config.slider_images %}
                <div class="relative border rounded-xl overflow-hidden bg-slate-50 shadow-sm">
                    <img src="{{ img }}" class="w-full aspect-[16/9] object-cover" alt="Slide {{ loop.index }}">
                    <div class="p-2 flex items-center justify-between bg-white text-[11px]">
                        <span class="font-bold text-slate-600">Slide {{ loop.index }}</span>
                        <form method="POST" onsubmit="return confirm('Kya aap is slide ko delete karna chahte hain?');">
                            <input type="hidden" name="action" value="delete_slider_img">
                            <input type="hidden" name="img_index" value="{{ loop.index0 }}">
                            <button type="submit" class="text-rose-600 hover:text-rose-800 font-bold">Delete</button>
                        </form>
                    </div>
                </div>
                {% else %}
                <p class="text-xs text-slate-400 col-span-3">Abhi koi photo add nahi hai.</p>
                {% endfor %}
            </div>
        </div>

        <!-- 2. Course Coupon & Price Manager -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
            <h2 class="font-bold text-indigo-700 flex items-center gap-1.5 mb-3 text-base">
                <span class="material-symbols-outlined">local_offer</span> Course Price & Coupon Codes
            </h2>
            <div class="space-y-3">
                {% for c in courses %}
                <form method="POST" class="flex flex-wrap sm:flex-nowrap items-center gap-2 p-2.5 border rounded-xl bg-slate-50 text-xs">
                    <input type="hidden" name="action" value="update_course">
                    <input type="hidden" name="course_id" value="{{ c.id }}">
                    <div class="w-full sm:w-1/3">
                        <p class="font-bold text-slate-800 truncate">{{ c.title }}</p>
                        <span class="text-[10px] text-slate-400">{{ c.badge }}</span>
                    </div>
                    <div class="w-1/3 sm:w-24">
                        <label class="text-[10px] text-slate-500 block">Price (₹)</label>
                        <input type="number" name="price" value="{{ c.price }}" class="w-full border rounded p-1.5 text-xs font-bold" required>
                    </div>
                    <div class="w-1/3 sm:w-28">
                        <label class="text-[10px] text-slate-500 block">Coupon</label>
                        <input type="text" name="coupon" value="{{ c.coupon }}" placeholder="DISCOUNT50" class="w-full border rounded p-1.5 text-xs uppercase font-mono">
                    </div>
                    <div class="w-full sm:w-auto mt-2 sm:mt-4">
                        <button type="submit" class="w-full bg-indigo-600 text-white font-bold px-3 py-1.5 rounded-lg text-xs">Save</button>
                    </div>
                </form>
                {% endfor %}
            </div>
        </div>

        <!-- 3. Live Class Setup -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
            <h2 class="font-bold text-red-600 mb-3 flex items-center gap-1.5 text-base">
                <span class="material-symbols-outlined">live_tv</span> Live Class YouTube Link
            </h2>
            <form method="POST" class="space-y-3 text-xs">
                <input type="hidden" name="action" value="update_live">
                <input type="text" name="live_title" value="{{ config.live_title }}" placeholder="Topic" class="w-full border p-2 rounded-lg" required>
                <input type="text" name="live_url" value="{{ config.live_url }}" placeholder="YouTube Link" class="w-full border p-2 rounded-lg" required>
                <label class="flex items-center gap-2">
                    <input type="checkbox" name="is_live" {% if config.is_live %}checked{% endif %}> Live Stream Student App me dikhayein
                </label>
                <button type="submit" class="bg-red-600 text-white font-bold px-4 py-2 rounded-lg">Update Live Video</button>
            </form>
        </div>

        <!-- 4. Add Test Series -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
            <h2 class="font-bold text-green-700 mb-3 flex items-center gap-1.5 text-base">
                <span class="material-symbols-outlined">add_task</span> Naya Test Banayein
            </h2>
            <form method="POST" class="flex gap-2 text-xs">
                <input type="hidden" name="action" value="create_test">
                <input type="text" name="title" placeholder="Test Name" class="w-2/3 border p-2 rounded-lg" required>
                <input type="number" name="duration" value="30" placeholder="Duration (Min)" class="w-1/3 border p-2 rounded-lg" required>
                <button type="submit" class="bg-green-600 text-white font-bold px-4 py-2 rounded-lg">Create</button>
            </form>
        </div>

        <!-- 5. Add Questions to Test -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
            <h2 class="font-bold text-blue-800 mb-3 flex items-center gap-1.5 text-base">
                <span class="material-symbols-outlined">quiz</span> Test me Sawal Jodein
            </h2>
            <form method="POST" class="space-y-3 text-xs">
                <input type="hidden" name="action" value="add_question">
                <select name="test_id" class="w-full border p-2 rounded-lg font-bold" required>
                    {% for t in tests %}
                    <option value="{{ t.id }}">{{ t.title }} ({{ t.questions|length }} Sawal)</option>
                    {% endfor %}
                </select>
                <textarea name="question" placeholder="Sawal likhein..." class="w-full border p-2 rounded-lg" required></textarea>
                <div class="grid grid-cols-2 gap-2">
                    <input type="text" name="opt_a" placeholder="Option A" class="border p-2 rounded" required>
                    <input type="text" name="opt_b" placeholder="Option B" class="border p-2 rounded" required>
                    <input type="text" name="opt_c" placeholder="Option C" class="border p-2 rounded" required>
                    <input type="text" name="opt_d" placeholder="Option D" class="border p-2 rounded" required>
                </div>
                <div class="flex gap-2">
                    <select name="answer" class="border p-2 rounded uppercase w-1/3 font-bold" required>
                        <option value="a">A</option><option value="b">B</option><option value="c">C</option><option value="d">D</option>
                    </select>
                    <input type="text" name="solution" placeholder="Vyakhya / Explanation" class="border p-2 rounded w-2/3">
                </div>
                <button type="submit" class="bg-blue-700 text-white font-bold px-4 py-2 rounded-lg">Sawal Add Karein</button>
            </form>
        </div>
    </main>
    {% endif %}

</body>
</html>
""",

    # 5. templates/index.html (With Dynamic Slider Display)
    "templates/index.html": """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
