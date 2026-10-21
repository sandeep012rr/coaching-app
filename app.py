import os
import json
import zipfile
from flask import Flask, render_template_string, request, redirect, url_for, session, send_file

app = Flask(__name__)
app.secret_key = "classplus_saas_super_secret_2026"

DATA_FILE = 'saas_database.json'

DEFAULT_DB = {
    "super_admin_pass": "master999",
    "client": {
        "app_name": "special education needs",
        "client_pass": "client123",
        "phone": "9828625119",
        "whatsapp_channel": "https://whatsapp.com/channel/0029VbBrZUT6LwHeVGFnvl3Q",
        "is_active": True,
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
            {"id": 3, "title": "KVS INTERVIEW PREPARATION", "price": 899, "orig_price": 999, "discount": "10% off", "coupon": "", "badge": "Interview"},
            {"id": 4, "title": "Punjab Special Education – Primary & Master Cadre", "price": 899, "orig_price": 1200, "discount": "Special Offer", "coupon": "", "badge": "New"},
            {"id": 5, "title": "Special Education All In One", "price": 10000, "orig_price": 15000, "discount": "33% off", "coupon": "", "badge": "Master Pack"},
            {"id": 6, "title": "Integrated Special and Inclusive Teacher Education (ISITEP)", "price": 10000, "orig_price": 15000, "discount": "33% off", "coupon": "", "badge": "ISITEP"},
            {"id": 7, "title": "Rajasthan 1st Grade School Lecturer (Special Education) 2026", "price": 1999, "orig_price": 2999, "discount": "Target Batch", "coupon": "RPSC26", "badge": "Batch 2026"},
            {"id": 8, "title": "DSSSB TGT SPECIAL EDUCATION", "price": 899, "orig_price": 1500, "discount": "40% off", "coupon": "", "badge": "Selection Batch"}
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
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(e)

STUDENT_HTML = """<!DOCTYPE html>
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
    <header class="sticky top-0 z-30 bg-white/95 backdrop-blur-md px-4 py-3 flex items-center justify-between border-b border-slate-100">
        <div class="flex items-center gap-2.5">
            <span class="material-symbols-outlined text-2xl text-slate-700">menu</span>
            <span class="text-base font-bold text-slate-800 tracking-tight lowercase">{{ db.client.app_name }}</span>
        </div>
        <div class="flex items-center gap-2">
            {% if student %}
            <span class="text-[11px] font-bold text-blue-800 bg-blue-50 px-2 py-1 rounded">{{ student.name }}</span>
            <a href="/logout" class="text-[10px] bg-slate-100 text-slate-600 font-bold px-2 py-1 rounded border">Logout</a>
            {% else %}
            <button onclick="document.getElementById('login-modal').classList.remove('hidden')" class="text-xs bg-blue-600 text-white font-bold px-3 py-1.5 rounded-lg shadow-sm">Login</button>
            {% endif %}
            <a href="/client" class="text-xs bg-indigo-50 text-indigo-700 font-bold px-2 py-1 rounded border border-indigo-200">Admin</a>
        </div>
    </header>

    <main class="max-w-lg mx-auto px-4 pt-3 space-y-4">
        <div class="flex items-center justify-between">
            <div>
                <h2 class="text-lg font-bold text-slate-900">Hello, {{ student.name if student else 'Neetu Meena' }} 👋</h2>
                <p class="text-xs text-slate-500">Welcome to {{ db.client.app_name }}</p>
            </div>
            <a href="/superadmin" class="text-[10px] bg-amber-100 text-amber-900 px-2 py-1 rounded font-bold border border-amber-300">Owner Panel</a>
        </div>

        {% if db.client.features.slider %}
        <div class="relative w-full rounded-2xl overflow-hidden shadow-sm border border-slate-200 bg-white">
            <div id="slider-track" class="flex transition-transform duration-500 ease-out" style="transform: translateX(0%);">
                <div class="w-full flex-shrink-0 p-4 bg-gradient-to-r from-amber-50 via-white to-blue-50">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="bg-red-600 text-white text-[10px] font-black uppercase px-2 py-0.5 rounded-full">Welcome</span>
                        <p class="text-xs font-semibold text-amber-800">आप सभी का परिवार में स्वागत है!</p>
                    </div>
                    <h3 class="text-sm font-bold text-slate-900">{{ db.content.welcome_title }}</h3>
                    <p class="text-[11px] text-slate-600 mt-1">{{ db.content.welcome_text }}</p>
                    <div class="mt-3 flex items-center justify-between pt-2 border-t border-slate-200/60 text-xs">
                        <a href="tel:{{ db.client.phone }}" class="flex items-center gap-1 font-bold text-blue-700">
                            <span class="material-symbols-outlined text-base">call</span> {{ db.client.phone }}
                        </a>
                        <a href="{{ db.client.whatsapp_channel }}" target="_blank" class="flex items-center gap-1 font-bold text-emerald-600">
                            <span class="material-symbols-outlined text-base">group</span> WhatsApp Channel
                        </a>
                    </div>
                </div>
                {% for img in db.content.slider_images %}
                <div class="w-full flex-shrink-0 aspect-[16/8] bg-slate-100">
                    <img src="{{ img }}" class="w-full h-full object-cover" alt="Slide {{ loop.index }}">
                </div>
                {% endfor %}
            </div>
            <button onclick="prevSlide()" class="absolute left-2 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-black/40 text-white flex items-center justify-center text-xs z-10">❮</button>
            <button onclick="nextSlide()" class="absolute right-2 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-black/40 text-white flex items-center justify-center text-xs z-10">❯</button>
        </div>
        {% endif %}

        {% if db.client.features.live_class and db.content.live.is_live %}
        <div class="bg-white rounded-2xl shadow-sm p-3.5 border border-red-100">
            <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 bg-red-600 rounded-full animate-ping"></span>
                    <span class="text-xs font-bold text-red-600 uppercase">Live Stream</span>
                </div>
            </div>
            <p class="text-xs font-semibold text-slate-800 mb-2">{{ db.content.live.title }}</p>
            <div class="relative w-full aspect-video rounded-xl overflow-hidden bg-black">
                <iframe class="w-full h-full" src="{{ db.content.live.url }}" frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
        {% endif %}

        <div class="grid grid-cols-3 gap-3 pt-1">
            {% if db.client.features.courses %}
            <div onclick="document.getElementById('courses-modal').classList.remove('hidden')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">school</span></div>
                <span class="text-xs font-medium text-slate-800">Courses</span>
            </div>
            {% endif %}

            <div onclick="openInfo('MY Timetable', '• 10:00 AM: RPwD Act Class<br>• 02:00 PM: Pedagogy<br>• 08:00 PM: Live Test')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">calendar_month</span></div>
                <span class="text-xs font-medium text-slate-800">MY Timetable</span>
            </div>

            <div onclick="openInfo('Latest Update', 'RPSC 1st Grade aur DSSSB Special Educator notifications live.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">newspaper</span></div>
                <span class="text-xs font-medium text-slate-800">Latest update</span>
            </div>

            <div onclick="window.scrollTo({top:0, behavior:'smooth'})" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-red-50 text-red-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">smart_display</span></div>
                <span class="text-xs font-medium text-slate-800">Youtube classes</span>
            </div>

            {% if db.client.features.notes_ebooks %}
            <div onclick="openInfo('Notes & PDFs', 'Handwritten Notes & PDFs available in batch.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">picture_as_pdf</span></div>
                <span class="text-xs font-medium text-slate-800">Notes & PDFs</span>
            </div>
            {% endif %}

            {% if db.client.features.tests %}
            <div onclick="document.getElementById('test-series-anchor').scrollIntoView({behavior:'smooth'})" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">quiz</span></div>
                <span class="text-xs font-semibold text-blue-900">Test Series</span>
            </div>
            {% endif %}

            {% if db.client.features.notes_ebooks %}
            <div onclick="openInfo('E-Book', 'Bilingual 7000+ MCQ E-Book Bank.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">menu_book</span></div>
                <span class="text-xs font-medium text-slate-800">E-Book</span>
            </div>
            {% endif %}

            <div onclick="document.getElementById('test-series-anchor').scrollIntoView({behavior:'smooth'})" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">assignment_turned_in</span></div>
                <span class="text-xs font-medium text-slate-800">Quiz</span>
            </div>

            <a href="tel:{{ db.client.phone }}" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">support_agent</span></div>
                <span class="text-xs font-medium text-slate-800">Contact & Help</span>
            </a>

            <div onclick="openInfo('Blog', 'Special Education Articles & Updates.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-cyan-50 text-cyan-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">article</span></div>
                <span class="text-xs font-medium text-slate-800">Blog</span>
            </div>

            <div onclick="openInfo('Current Affairs', 'Disability & RCI Latest News 2026.')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">public</span></div>
                <span class="text-xs font-medium text-slate-800">Current Affairs</span>
            </div>

            <div onclick="openInfo('1 to 1 Mentorship', 'Direct Guidance: {{ db.client.phone }}')" class="app-card bg-white rounded-2xl p-3 flex flex-col items-center justify-center text-center cursor-pointer min-h-[92px]">
                <div class="w-11 h-11 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center mb-1.5"><span class="material-symbols-outlined">group</span></div>
                <span class="text-xs font-medium text-slate-800">1 to 1 section</span>
            </div>
        </div>

        {% if db.client.features.tests %}
        <div id="test-series-anchor" class="pt-2">
            <h3 class="text-base font-bold text-slate-800 mb-3 flex items-center gap-1.5">
                <span class="material-symbols-outlined text-blue-700">fact_check</span> Active Test Series
            </h3>
            <div class="space-y-2.5">
                {% for test in db.content.tests %}
                <div class="bg-white rounded-xl p-3.5 border border-slate-200 shadow-sm flex items-center justify-between">
                    <div>
                        <h4 class="text-sm font-bold text-slate-900">{{ test.title }}</h4>
                        <p class="text-xs text-slate-500 mt-0.5">⏱️ {{ test.duration }} Min | {{ test.questions|length }} Sawal</p>
                    </div>
                    <a href="/test/{{ test.id }}" class="bg-blue-600 text-white text-xs font-bold px-4 py-2 rounded-lg shadow-sm">Start Test</a>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </main>

    {% if db.client.features.courses %}
    <div id="courses-modal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm hidden flex items-end sm:items-center justify-center">
        <div class="bg-white rounded-t-3xl sm:rounded-2xl max-w-lg w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            <div class="p-4 border-b flex items-center justify-between bg-slate-50">
                <h3 class="font-bold text-slate-800 text-base">All Special Education Courses</h3>
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
                            <span class="inline-block mt-1 text-[10px] bg-indigo-50 text-indigo-700 font-bold px-2 py-0.5 rounded border border-indigo-200">🎟️ Coupon: {{ c.coupon }}</span>
                            {% endif %}
                        </div>
                        <span class="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">{{ c.discount }}</span>
                    </div>
                    <div class="flex justify-between items-center pt-1">
                        <div>
                            <span class="text-base font-extrabold text-slate-900">₹{{ c.price }}</span>
                            <span class="text-xs text-slate-400 line-through ml-1">₹{{ c.orig_price }}</span>
                        </div>
                        <a href="https://wa.me/91{{ db.client.phone }}?text=Mujhe%20{{ c.title }}%20join%20karna%20hai" target="_blank" class="bg-blue-600 text-white text-xs font-bold px-4 py-1.5 rounded-lg">Join Now</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
  
