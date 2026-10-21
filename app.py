import os
import json
import zipfile
from flask import Flask, render_template_string, request, redirect, url_for, session, send_file

app = Flask(__name__)
app.secret_key = "classplus_saas_super_secret_2026"

DATA_FILE = 'saas_database.json'

# Default Master Database (3-Layer Architecture)
DEFAULT_DB = {
    "super_admin_pass": "master999",
    "client": {
        "app_name": "special education needs",
        "client_pass": "client123",
        "phone": "9828625119",
        "whatsapp_channel": "https://whatsapp.com/channel/0029VbBrZUT6LwHeVGFnvl3Q",
        "is_active": True,  # Super admin can suspend app if False
        "features": {
            "slider": True,
            "live_class": True,
            "courses": True,
            "tests": True,
            "notes_ebooks": True
        }
    },
    "content": {
        "welcome_title": "SPECIAL EDUCATION NEEDS",
        "welcome_text": "हम आपके हर कदम में साथ हैं! RPSC, DSSSB, REET और KVS Special Education भर्ती परीक्षा की सम्पूर्ण तैयारी।",
        "slider_images": [
            "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800&auto=format&fit=crop"
        ],
        "live": {
            "is_live": True,
            "title": "Special Education Live Marathon Class",
            "url": "https://www.youtube-nocookie.com/embed/live_stream"
        },
        "courses": [
            {"id": 1, "title": "SPECIAL EDUCATION MCQ BATCH", "price": 1199, "orig_price": 2199, "discount": "45% off", "coupon": "SPEC50", "badge": "New"},
            {"id": 2, "title": "DSSSB PRT SPECIAL EDUCATION", "price": 899, "orig_price": 1500, "discount": "Selection Batch", "coupon": "", "badge": "Hot"},
            {"id": 3, "title": "Rajasthan 1st Grade Special Edu 2026", "price": 1999, "orig_price": 2999, "discount": "Target Batch", "coupon": "RPSC26", "badge": "Batch 2026"}
        ],
        "tests": [
            {
                "id": 1,
                "title": "RPwD Act 2016 Mock Test - 01",
                "duration": 30,
                "questions": [
                    {
                        "question": "RPwD Act 2016 me kul kitni disabilities shamil hain?",
                        "options": ["7 Disabilities", "14 Disabilities", "21 Disabilities", "25 Disabilities"],
                        "answer": "c",
                        "solution": "RPwD Act 2016 me 7 se badha kar 21 disabilities kar di gayi hain."
                    }
                ]
            }
        ],
        "students": []
    }
}

def load_db():
    if not os.path.exists(DATA_FILE):
        save_db(DEFAULT_DB)
        return DEFAULT_DB
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DB

def save_db(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==========================================================
# HTML TEMPLATES (Embedded to prevent TemplateNotFound Error)
# ==========================================================

# 1. LAYER 3: STUDENT APP TEMPLATE
STUDENT_HTML = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ db.client.app_name }}</title>
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

    {% if not db.client.is_active %}
    <div class="min-h-screen flex items-center justify-center p-6 text-center bg-slate-900 text-white">
        <div class="max-w-sm space-y-3">
            <span class="material-symbols-outlined text-5xl text-red-500">lock</span>
            <h1 class="text-xl font-bold">App Temporarily Suspended</h1>
            <p class="text-xs text-slate-400">Is coaching portal ki subscription avadhi samapt ho gayi hai. Kripya Master Developer se sampark karein.</p>
        </div>
    </div>
    {% else %}

    <!-- Top App Bar -->
    <header class="sticky top-0 z-30 bg-white/95 backdrop-blur-md px-4 py-3 flex items-center justify-between border-b border-slate-100">
        <div class="flex items-center gap-2.5">
            <span class="material-symbols-outlined text-2xl text-blue-700">school</span>
            <span class="text-base font-bold text-slate-800 tracking-tight lowercase">{{ db.client.app_name }}</span>
        </div>
        <div class="flex items-center gap-2">
            {% if student %}
            <span class="text-[11px] font-bold text-blue-800 bg-blue-50 px-2 py-1 rounded">{{ student.name }}</span>
            <a href="/logout" class="text-[10px] bg-slate-100 text-slate-600 font-bold px-2 py-1 rounded border">Logout</a>
            {% else %}
            <button onclick="document.getElementById('login-modal').classList.remove('hidden')" class="text-xs bg-blue-600 text-white font-bold px-3 py-1.5 rounded-lg shadow-sm">Student Login</button>
            {% endif %}
        </div>
    </header>

    <main class="max-w-lg mx-auto px-4 pt-3 space-y-4">

        <!-- Greeting -->
        <div class="flex items-center justify-between">
            <div>
                <h2 class="text-lg font-bold text-slate-900">Hello, {{ student.name if student else 'Aspirant' }} 👋</h2>
                <p class="text-xs text-slate-500">Welcome to {{ db.client.app_name }}</p>
            </div>
            <div class="flex gap-1">
                <a href="/client" class="text-[10px] bg-slate-200 text-slate-700 px-2 py-1 rounded font-semibold">Teacher Login</a>
            </div>
        </div>

        <!-- Dynamic Image Slider (If Allowed by Super Admin) -->
        {% if db.client.features.slider %}
        <div class="relative w-full rounded-2xl overflow-hidden shadow-sm border border-slate-200 bg-white">
            <div id="slider-track" class="flex transition-transform duration-500 ease-out" style="transform: translateX(0%);">
                
                <!-- Slide 1: Welcome Card -->
                <div class="w-full flex-shrink-0 p-4 bg-gradient-to-r from-amber-50 via-white to-blue-50">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="bg-red-600 text-white text-[10px] font-black uppercase px-2 py-0.5 rounded-full">Welcome</span>
                        <p class="text-xs font-semibold text-amber-800">आप सभी का स्वागत है!</p>
                    </div>
                    <h3 class="text-sm font-bold text-slate-900">{{ db.content.welcome_title }}</h3>
                    <p class="text-[11px] text-slate-600 mt-1">{{ db.content.welcome_text }}</p>
                    <div class="mt-3 flex items-center justify-between pt-2 border-t border-slate-200/60 text-xs">
                        <a href="tel:{{ db.client.phone }}" class="flex items-center gap-1 font-bold text-blue-700">
                            <span class="material-symbols-outlined text-base">call</span> {{ db.client.phone }}
                        </a>
                        <a href="{{ db.client.whatsapp_channel }}" target="_blank" class="flex items-center gap-1 font-bold text-emerald-600">
                            <span class="material-symbols-outlined text-base">group</span> WhatsApp Group
                        </a>
                    </div>
                </div>

                <!-- Client Uploaded Images -->
                {% for img in db.content.slider_images %}
                <div class="w-full flex-shrink-0 aspect-[16/8] bg-slate-100">
                    <img src="{{ img }}" class="w-full h-full object-cover" alt="Slide {{ loop.index }}">
                </div>
                {% endfor %}
            </div>

            <button onclick="prevSlide()" class="absolute left-2 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-black/40 text-white flex items-center justify-center text-xs z-10">❮</button>
            <button onclick="nextSlide()" class="absolute right-2 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-black/40 text-white flex items-center justify-center text-xs z-10">❯</button>
            <div id="slider-dots" class="absolute bottom-2 left-1/2 -translate-x-1/2 flex items-center gap-1.5 z-10"></div>
        </div>
        {% endif %}

        <!-- Live Class Player (If Allowed by Super Admin & Active) -->
        {% if db.client.features.live_class and db.content.live.is_live %}
        <div class="bg-white rounded-2xl shadow-sm p-3.5 border border-red-100">
            <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 bg-red-600 rounded-full animate-ping"></span>
                    <span class="text-xs font-bold text-red-600 uppercase">Live Class</span>
                </div>
                <span class="text-[10px] text-slate-400">Streaming Now</span>
            </div>
            <p class="text-xs font-semibold text-slate-800 mb-2">{{ db.content.live.title }}</p>
            <div class="relative w-full aspect-video rounded-xl overflow-hidden bg-black">
                <iframe class="w-full h-full" src="{{ db.content.live.url }}" frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
        {% endif %}

        <!-- App Feature Grid Buttons -->
        <div class="grid grid-cols-3 gap-3 pt-1">
            {% if db.client.features.courses %}
            <div onclick="document.getElementById('courses-modal').classList.remove('hidden')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">school</span></div>
                <span class="text-xs font-semibold text-slate-800">Courses</span>
            </div>
            {% endif %}

            {% if db.client.features.tests %}
            <div onclick="document.getElementById('test-series-anchor').scrollIntoView({behavior:'smooth'})" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">quiz</span></div>
                <span class="text-xs font-semibold text-slate-800">Test Series</span>
            </div>
            {% endif %}

            {% if db.client.features.notes_ebooks %}
            <div onclick="openInfo('Notes & PDFs', 'Handwritten Notes aur PDFs jald hi aapke batch me judenge.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">picture_as_pdf</span></div>
                <span class="text-xs font-semibold text-slate-800">Notes & PDFs</span>
            </div>
            <div onclick="openInfo('E-Books Bank', 'Bilingual 7000+ MCQ E-Book aur Study Modules.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">menu_book</span></div>
                <span class="text-xs font-semibold text-slate-800">E-Books</span>
            </div>
            {% endif %}

            <div onclick="openInfo('Daily Timetable', '• Morning 10 AM: Theory Class<br>• Evening 8 PM: Live MCQ Test')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">calendar_month</span></div>
                <span class="text-xs font-semibold text-slate-800">Timetable</span>
            </div>

            <a href="tel:{{ db.client.phone }}" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">support_agent</span></div>
                <span class="text-xs font-semibold text-slate-800">Help Desk</span>
            </a>
        </div>

        <!-- CBT Test Series Section (If Allowed by Super Admin) -->
        {% if db.client.features.tests %}
        <div id="test-series-anchor" class="pt-2">
            <h3 class="text-base font-bold text-slate-800 mb-3 flex items-center gap-1.5">
                <span class="material-symbols-outlined text-blue-700">fact_check</span> Online CBT Test Series
            </h3>
            <div class="space-y-2.5">
                {% for test in db.content.tests %}
                <div class="bg-white rounded-xl p-3.5 border border-slate-200 shadow-sm flex items-center justify-between">
                    <div>
                        <h4 class="text-sm font-bold text-slate-900">{{ test.title }}</h4>
                        <p class="text-xs text-slate-500 mt-0.5">⏱️ {{ test.duration }} Min | {{ test.questions|length }} Questions</p>
                    </div>
                    <a href="/test/{{ test.id }}" class="bg-blue-600 text-white text-xs font-bold px-4 py-2 rounded-lg shadow-sm">Start Test</a>
                </div>
                {% else %}
                <div class="bg-white p-5 rounded-xl text-center text-xs text-slate-400 border border-dashed">No active tests yet.</div>
                {% endfor %}
            </div>
        </div>
        {% endif %}

    </main>

    <!-- Courses Modal -->
    {% if db.client.features.courses %}
    <div id="courses-modal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm hidden flex items-end sm:items-center justify-center">
        <div class="bg-white rounded-t-3xl sm:rounded-2xl max-w-lg w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            <div class="p-4 border-b flex items-center justify-between bg-slate-50">
                <h3 class="font-bold text-slate-800 text-base">Available Courses & Batches</h3>
                <button onclick="document.getElementById('courses-modal').classList.add('hidden')" class="w-8 h-8 rounded-full bg-slate-200 font-bold">✕</button>
            </div>
            <div class="p-4 overflow-y-auto space-y-3">
                {% for c in db.content.courses %}
                <div class="border rounded-xl p-3.5 bg-white shadow-sm space-y-2">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="bg-amber-100 text-amber-800 text-[10px] font-bold px-2 py-0.5 rounded">{{ c.badge }}</span>
                            <h4 class="font-bold text-slate-900 text-sm mt-1">{{ c.title }}</h4>
                            {% if c.coupon %}
                            <span class="inline-block mt-1 text-[10px] bg-indigo-50 text-indigo-700 font-bold px-2 py-0.5 rounded border border-indigo-200">🎟️ Use Code: {{ c.coupon }}</span>
                            {% endif %}
                        </div>
                        <span class="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">{{ c.discount }}</span>
                    </div>
                    <div class="flex justify-between items-center pt-1">
                        <div>
                            <span class="text-base font-extrabold text-slate-900">₹{{ c.price }}</span>
                            <span class="text-xs text-slate-400 line-through ml-1">₹{{ c.orig_price }}</span>
                        </div>
                        <a href="https://wa.me/91{{ db.client.phone }}?text=Mujhe%20{{ c.title }}%20join%20karna%20hai" target="_blank" class="bg-blue-600 text-white text-xs font-bold px-4 py-1.5 rounded-lg">Buy Now</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    {% endif %}

    <!-- Student Login Modal -->
    <div id="login-modal" class="fixed inset-0 z-50 bg-black/60 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-sm w-full p-6 space-y-4">
            <div class="flex justify-between items-center">
                <h3 class="font-bold text-base">Student Login / Register</h3>
                <button onclick="document.getElementById('login-modal').classList.add('hidden')">✕</button>
            </div>
            <form action="/student_auth" method="POST" class="space-y-3 text-xs">
                <input type="text" name="name" placeholder="Apna Naam" class="w-full border p-2.5 rounded-xl" required>
                <input type="tel" name="phone" placeholder="Mobile Number" class="w-full border p-2.5 rounded-xl" required>
                <button type="submit" class="w-full bg-blue-600 text-white font-bold py-2.5 rounded-xl">Continue to App</button>
            </form>
        </div>
    </div>

    <!-- Info Modal -->
    <div id="info-modal" class="fixed inset-0 z-50 bg-black/50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-sm w-full p-5 space-y-3">
            <h4 id="info-title" class="font-bold text-base"></h4>
            <div id="info-body" class="text-xs text-slate-600"></div>
            <button onclick="document.getElementById('info-modal').classList.add('hidden')" class="w-full bg-blue-600 text-white text-xs font-bold py-2 rounded-xl">Close</button>
        </div>
    </div>

    <script>
        let currentSlide = 0;
        const track = document.getElementById('slider-track');
        const totalSlides = track ? track.children.length : 0;
        function updateSlider() { if (track) track.style.transform = `translateX(-${currentSlide * 100}%)`; }
        function nextSlide() { if (totalSlides > 1) { currentSlide = (currentSlide + 1) % totalSlides; updateSlider(); } }
        function prevSlide() { if (totalSlides > 1) { currentSlide = (currentSlide - 1 + totalSlides) % totalSlides; updateSlider(); } }
        if (totalSlides > 1) setInterval(nextSlide, 3500);
        function openInfo(t, b) {
            document.getElementById('info-title').innerHTML = t;
            document.getElementById('info-body').innerHTML = b;
            document.getElementById('info-modal').classList.remove('hidden');
        }
    </script>
    {% endif %}
</body>
</html>
"""

# 2. LAYER 2: CLIENT / TEACHER ADMIN PANEL TEMPLATE
CLIENT_HTML = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teacher / Client Panel - {{ db.client.app_name }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
</head>
<body class="bg-slate-100 min-h-screen pb-16 font-s
