import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
TESTS_FILE = 'tests.json'
CONFIG_FILE = 'config.json'

def load_data():
    if not os.path.exists(TESTS_FILE):
        with open(TESTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    with open(TESTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(TESTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "live_title": "Special Education Live Class",
            "live_url": "https://www.youtube-nocookie.com/embed/live_stream",
            "is_live": True
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    tests = load_data()
    config = load_config()
    return render_template('index.html', tests=tests, config=config)

@app.route('/test/<int:test_id>')
def take_test(test_id):
    tests = load_data()
    target_test = next((t for t in tests if t['id'] == test_id), None)
    if not target_test:
        return "Test nahi mila!", 404
    return render_template('test.html', test=target_test)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    tests = load_data()
    config = load_config()

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

            if video_id:
                config['live_url'] = f"https://www.youtube-nocookie.com/embed/{video_id}"
            else:
                config['live_url'] = raw_url

            config['live_title'] = request.form.get('live_title')
            config['is_live'] = 'is_live' in request.form
            save_config(config)

        elif action == 'create_test':
            title = request.form.get('title')
            duration = int(request.form.get('duration', 30))
            new_test = {
                "id": len(tests) + 1,
                "title": title,
                "duration": duration,
                "questions": [
                    {
                        "question": "दिव्यांगजन अधिकार अधिनियम (RPwD Act) किस वर्ष लागू किया गया था?",
                        "options": ["2014", "2016", "2018", "2020"],
                        "answer": "b",
                        "solution": "RPwD Act 2016 में संसद द्वारा पारित हुआ और लागू किया गया।"
                    }
                ]
            }
            tests.append(new_test)
            save_data(tests)

        return redirect(url_for('admin'))

    return render_template('admin.html', tests=tests, config=config)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
              
