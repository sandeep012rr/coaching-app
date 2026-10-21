import os
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
                return render_template('login.html', error="Mobile number pehle se registered hai!")
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

# Admin Control Panel
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

        # 1. Slider me image add karna
        if action == 'add_slider_img':
            img_url = request.form.get('img_url', '').strip()
            if img_url:
                if 'slider_images' not in config:
                    config['slider_images'] = []
                if len(config['slider_images']) < 10:
                    config['slider_images'].append(img_url)
                    save_json(CONFIG_FILE, config)

        # 2. Slider se image hatana
        elif action == 'delete_slider_img':
            img_index = int(request.form.get('img_index'))
            if 'slider_images' in config and 0 <= img_index < len(config['slider_images']):
                config['slider_images'].pop(img_index)
                save_json(CONFIG_FILE, config)

        # 3. Live video stream update karna
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

        # 4. Naya test series banana
        elif action == 'create_test':
            new_test = {
                "id": len(tests) + 1,
                "title": request.form.get('title'),
                "duration": int(request.form.get('duration', 30)),
                "questions": []
            }
            tests.append(new_test)
            save_json(TESTS_FILE, tests)

        # 5. Sawal jodna
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

        # 6. Course price aur coupon set karna
        elif action == 'update_course':
            c_id = int(request.form.get('course_id'))
            for c in courses:
                if c['id'] == c_id:
                    c['price'] = int(request.form.get('price'))
                    c['coupon'] = request.form.get('coupon', '').strip()
                    c['discount'] = request.form.get('discount', '').strip()
                    break
            save_json(COURSES_FILE, courses)

        # 7. Test delete karna
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
