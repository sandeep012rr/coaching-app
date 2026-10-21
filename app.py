import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "special_education_admin_secret_key_2026"

# Admin Login Password
ADMIN_PASSWORD = "admin123"  # Yahan aap apna secret password badal sakte hain

TESTS_FILE = 'tests.json'
CONFIG_FILE = 'config.json'
COURSES_FILE = 'courses.json'

def load_json(filepath, default_data):
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return default_data

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Default courses from screenshot
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
    "banner_title": "SPECIAL EDUCATION NEEDS",
    "banner_text": "हम आपके हर कदम में साथ हैं! RPSC, DSSSB, REET और KVS Special Education भर्ती परीक्षा की सम्पूर्ण तैयारी।",
    "contact_phone": "9828625119",
    "channel_code": "0029VbBrZUT6LwHeVGFnvl3Q"
}

# Student Portal View
@app.route('/')
def home():
    tests = load_json(TESTS_FILE, [])
    config = load_json(CONFIG_FILE, DEFAULT_CONFIG)
    courses = load_json(COURSES_FILE, DEFAULT_COURSES)
    return render_template('index.html', tests=tests, config=config, courses=courses)

@app.route('/test/<int:test_id>')
def take_test(test_id):
    tests = load_json(TESTS_FILE, [])
    target_test = next((t for t in tests if t['id'] == test_id), None)
    if not target_test:
        return "Test nahi mila!", 404
    return render_template('test.html', test=target_test)

# Secure Admin Login & Dashboard
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Login verification
    if request.method == 'POST' and request.form.get('action') == 'login':
        pwd = request.form.get('password')
        if pwd == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('admin.html', logged_in=False, error="Galat Password! Kripya sahi password dalein.")

    # Agar login nahi hai toh login screen dikhao
    if not session.get('is_admin'):
        return render_template('admin.html', logged_in=False)

    # Data load
    tests = load_json(TESTS_FILE, [])
    config = load_json(CONFIG_FILE, DEFAULT_CONFIG)
    courses = load_json(COURSES_FILE, DEFAULT_COURSES)

    if request.method == 'POST':
        action = request.form.get('action')

        # 1. Update Live Class
        if action == 'update_live':
            raw_url = request.form.get('live_url', '').strip()
            video_id = ""
            if "watch?v=" in raw_url:
                video_id = raw_url.split("watch?v=")[1].split("&")[0]
            elif "youtu.be/" in raw_url:
                video_id = raw_url.split("youtu.be/")[1].split("?")[0]
            elif "embed/" in raw_url:
                video_id = raw_url.split("embed/")[1].split("?")[0]

            if video_id:
                config['live_url'] = f"https://www.youtube-nocookie.com/embed/{video_id}"
            else:
                config['live_url'] = raw_url

            config['live_title'] = request.form.get('live_title')
            config['is_live'] = 'is_live' in request.form
            save_json(CONFIG_FILE, config)

        # 2. Add New Test Series
        elif action == 'create_test':
            title = request.form.get('title')
            duration = int(request.form.get('duration', 30))
            new_test = {
                "id": len(tests) + 1,
                "title": title,
                "duration": duration,
                "questions": []
            }
            tests.append(new_test)
            save_json(TESTS_FILE, tests)

        # 3. Add Single Question to a Test
        elif action == 'add_question':
            test_id = int(request.form.get('test_id'))
            q_text = request.form.get('question')
            opt_a = request.form.get('opt_a')
            opt_b = request.form.get('opt_b')
            opt_c = request.form.get('opt_c')
            opt_d = request.form.get('opt_d')
            ans = request.form.get('answer').lower()
            sol = request.form.get('solution', '')

            for t in tests:
                if t['id'] == test_id:
                    t['questions'].append({
                        "question": q_text,
                        "options": [opt_a, opt_b, opt_c, opt_d],
                        "answer": ans,
                        "solution": sol
                    })
                    break
            save_json(TESTS_FILE, tests)

        # 4. Update Course Price & Coupon
        elif action == 'update_course':
            c_id = int(request.form.get('course_id'))
            new_price = int(request.form.get('price'))
            coupon = request.form.get('coupon', '').strip()
            discount = request.form.get('discount', '').strip()

            for c in courses:
                if c['id'] == c_id:
                    c['price'] = new_price
                    c['coupon'] = coupon
                    if discount:
                        c['discount'] = discount
                    break
            save_json(COURSES_FILE, courses)

        # 5. Delete Test
        elif action == 'delete_test':
            t_id = int(request.form.get('test_id'))
            tests = [t for t in tests if t['id'] != t_id]
            save_json(TESTS_FILE, tests)

        return redirect(url_for('admin'))

    return render_template('admin.html', logged_in=True, tests=tests, config=config, courses=courses)

@app.route('/admin/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
