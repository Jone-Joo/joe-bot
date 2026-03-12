from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# سيرفر صغير عشان Render ميوقفش البوت على الـ Free Tier
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass

def run_ping_server():
    port = int(os.getenv("PORT", 8080))
    HTTPServer(("0.0.0.0", port), PingHandler).serve_forever()

# ============================================================
# الإعدادات الأساسية
# ============================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")   # مش هتكتب التوكن هنا تاني - هيجي من السيرفر
ADMIN_ID = 5169806405
USERS_FILE = "users.txt"

# ============================================================
# حفظ وتحميل المستخدمين
# ============================================================
def load_users():
    if not os.path.exists(USERS_FILE):
        return set()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return set(int(line.strip()) for line in f if line.strip().isdigit())

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        for user_id in users:
            f.write(str(user_id) + "\n")

USERS = load_users()

# ============================================================
# رسالة الترحيب
# ============================================================
START_MESSAGE = """
أكثروا من ذكر الله وحافظوا على الصلاة
وصلوا على حبيبنا ونبينا محمد 💕💕

📚 ذاكر كويس وافتكر دايمًا إن العلم قوة

📚 *دعـــاء المذاكـــرة* 📚
اللهم انا نسألك فهم النبيين وحفظ المرسلين والملائكة المقربين
بسم الله اللهم لا سهل إلا ما جعلته سهلاً وأنت تجعل الحزن إذا شئت سهلا

اختار السنة الدراسية من تحت ⬇️
"""

# ============================================================
# المواد الدراسية
# ⚠️ الترم الثاني: ضيف الروابط في أماكن LINK_HERE
# ============================================================
MATERIALS = {
    "سنة ثانية": {
        "الترم الأول": {
            "C++": {
                "PDFs": "https://drive.google.com/drive/folders/17U6K2p_fLzTSQ5brCCHqyQVM2QDV5rzL",
                "فيديوهات": "https://www.youtube.com/playlist?list=PL8DDsWuvM_EV9tIIZ_SrwCDnfTUmk_FRw",
                "موقع": "https://www.learncpp.com/"
            },
            "Database": {
                "PDFs": "https://drive.google.com/drive/folders/1rKknd3TsCRHbSk966tsVmJv-j1vQHqwx",
                "فيديوهات": "https://www.youtube.com/playlist?list=PLwCMLs3sjOY5YtF2jRxUN2x-3mJ3j3D9C",
                "موقع": "https://www.w3schools.com/sql/"
            },
            "Digital Engineering": {
                "PDFs": "https://drive.google.com/drive/folders/1aEl0pe0znjUU9gSiXkAxxRQzey5TUB_x",
                "فيديوهات": "https://www.youtube.com/playlist?list=PLbRMhDVUMngcOJzC4cKkjcOvR4Xr3iLWB",
                "موقع": "https://www.electronics-tutorials.ws/digital/digital_1.html"
            },
            "OS": {
                "PDFs": "https://drive.google.com/drive/folders/1wCuAmocwY7F5ihhgpLbxflDI57B-MtqY",
                "فيديوهات": "https://www.youtube.com/playlist?list=PLTr1xN4uMK5seRz6IO7Am9Zp2UKdnzO_n",
                "موقع": "https://www.tutorialspoint.com/operating_system/index.htm"
            },
            "WEB": {
                "PDFs": "https://drive.google.com/drive/folders/153ZjFBCSo8vUzBLJinWnSosE4aLm6Yvg",
                "فيديوهات": "https://youtu.be/MzouYpxPl0Y?si=mSMxuPVC7eFVVNdM",
                "موقع": "https://www.w3schools.com/html/"
            }
        },
        "الترم الثاني": {
            "CCNA": {
                "PDFs": "https://drive.google.com/drive/folders/1IR0OtkwuQ9Qmg2WOYoIASMyg9Z7vuQdG?usp=drive_link",
                "فيديوهات": "https://www.youtube.com/playlist?list=PLF1hDMPPRqGxpYdo0ctaa7MxfOi9vjs1u",
                "موقع": "https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html"
            },
            "Database": {
                "PDFs": "https://drive.google.com/drive/folders/1_9hw8I2HSmOqn6mffCd6omVAipIqg7Vy?usp=sharing",
                "فيديوهات": "https://www.youtube.com/playlist?list=PLwCMLs3sjOY5YtF2jRxUN2x-3mJ3j3D9C",
                "موقع": "https://www.w3schools.com/sql/"
            },
            "Data Structure": {
                "PDFs": "https://drive.google.com/drive/folders/1OJ2qBz5zpUtDrf2KmKObkvI7hbaaePsG?usp=drive_link",
                "فيديوهات": "https://www.youtube.com/playlist?list=PLPt2dINI2MIbmnCMnXMhksPQ4qH5A0k3I",
                "موقع": "https://visualgo.net/en"
            },
            "Java": {
                "PDFs": "https://drive.google.com/drive/folders/1qg-uX2yr9Atm23M_8N2rhhUeUruDVg11?usp=drive_link",
                "فيديوهات": "https://www.youtube.com/playlist?list=PLCInYL3l2AajYlZGzU_LVrHdoouf8W5dE",
                "موقع": "https://www.w3schools.com/java/"
            },
            "WEB 2": {
                "PDFs": "https://drive.google.com/drive/folders/1pv7BUqRI_VGSzgGBTeH6rcWpqb3N-KYc?usp=drive_link",
                "فيديوهات": "https://www.youtube.com/playlist?list=PLDoPjvoNmBAzHSjcR-HnW9tnxyuye8KbF",
                "موقع": "https://www.w3schools.com/js/"
            }
        }
    }
}

# ============================================================
# أسئلة الاختبار
# ============================================================
QUIZ_QUESTIONS = [
    {"q": "ما نوع البيانات الذي يستخدم لتخزين عدد صحيح في C++؟", "a": "int", "o": ["float", "int", "char", "string"]},
    {"q": "أي نظام مسؤول عن إدارة قواعد البيانات؟", "a": "DBMS", "o": ["OS", "DBMS", "Compiler", "Web Server"]},
    {"q": "ما هي لغة الترميز المستخدمة في بناء صفحات الويب؟", "a": "HTML", "o": ["Python", "HTML", "C++", "Java"]},
    {"q": "ما هو نظام التشغيل المسؤول عن إدارة موارد الحاسوب؟", "a": "Operating System", "o": ["Database", "Compiler", "Operating System", "Web Browser"]},
    {"q": "أي من التالي يستخدم لتصميم الدوائر الرقمية؟", "a": "Digital Logic", "o": ["Photoshop", "Digital Logic", "Word", "Excel"]}
]

# ============================================================
# القوائم (الأزرار)
# ============================================================
def main_menu_kb(user_id):
    buttons = [
        [InlineKeyboardButton("📘 سنة أولى", callback_data="year1")],
        [InlineKeyboardButton("📗 سنة ثانية", callback_data="year2")],
        [InlineKeyboardButton("🎯 اختبار شامل", callback_data="quiz_start")],
        [InlineKeyboardButton("📤 شارك البوت", callback_data="share")],
        [InlineKeyboardButton("📞 الدعم الفني", callback_data="support"),
         InlineKeyboardButton("ℹ️ معلومات", callback_data="info")],
    ]
    if user_id == ADMIN_ID:
        buttons.append([InlineKeyboardButton("📊 إحصائيات", callback_data="stats"),
                        InlineKeyboardButton("📢 نشر إعلان", callback_data="broadcast_mode")])
    return InlineKeyboardMarkup(buttons)

def terms_kb():
    buttons = [
        [InlineKeyboardButton("📚 الترم الأول", callback_data="term|سنة ثانية|الترم الأول")],
        [InlineKeyboardButton("📚 الترم الثاني", callback_data="term|سنة ثانية|الترم الثاني")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(buttons)

def subjects_kb(year, term):
    subjects = MATERIALS[year][term]
    buttons = [[InlineKeyboardButton(s, callback_data=f"subject|{year}|{term}|{s}")] for s in subjects]
    buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="year2")])
    return InlineKeyboardMarkup(buttons)

def subject_refs_kb(year, term, subject):
    refs = MATERIALS[year][term][subject]
    buttons = [
        [InlineKeyboardButton("📄 PDFs", url=refs["PDFs"])],
        [InlineKeyboardButton("🎥 فيديوهات", url=refs["فيديوهات"])],
        [InlineKeyboardButton("🌍 موقع", url=refs["موقع"])],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"term|{year}|{term}")]
    ]
    return InlineKeyboardMarkup(buttons)

def quiz_question_kb(options, index):
    return InlineKeyboardMarkup([[InlineKeyboardButton(o, callback_data=f"quiz_ans|{index}|{o}")] for o in options])

# ============================================================
# الأوامر
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USERS:
        USERS.add(user_id)
        save_users(USERS)
    await update.message.reply_text(START_MESSAGE, reply_markup=main_menu_kb(user_id), parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    await query.answer()

    # ── رجوع للقائمة الرئيسية
    if data == "back_main":
        await query.edit_message_text(START_MESSAGE, reply_markup=main_menu_kb(user_id), parse_mode='Markdown')

    # ── سنة أولى (قريباً)
    elif data == "year1":
        await query.edit_message_text(
            "📘 *سنة أولى*\n\n⏳ قريباً إن شاء الله سيتم إضافة مواد السنة الأولى!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]]),
            parse_mode='Markdown'
        )

    # ── سنة ثانية - اختار الترم
    elif data == "year2":
        await query.edit_message_text("📗 *سنة ثانية*\nاختار الترم:", reply_markup=terms_kb(), parse_mode='Markdown')

    # ── اختار الترم - اعرض المواد
    elif data.startswith("term|"):
        _, year, term = data.split("|", 2)
        await query.edit_message_text(
            f"📚 *{year} — {term}*\nاختار المادة:",
            reply_markup=subjects_kb(year, term),
            parse_mode='Markdown'
        )

    # ── اختار المادة - اعرض المراجع
    elif data.startswith("subject|"):
        parts = data.split("|", 3)
        _, year, term, subject = parts
        await query.edit_message_text(
            f"📘 *{subject}*\nاختار المرجع اللي يناسبك:",
            reply_markup=subject_refs_kb(year, term, subject),
            parse_mode='Markdown'
        )

    # ── الاختبار
    elif data == "quiz_start":
        context.user_data["score"] = 0
        await send_quiz_question(query, 0)

    elif data.startswith("quiz_ans|"):
        _, index, answer = data.split("|", 2)
        index = int(index)
        question = QUIZ_QUESTIONS[index]
        score = context.user_data.get("score", 0)
        if answer == question["a"]:
            score += 1
            await query.message.reply_text("✅ إجابة صحيحة!")
        else:
            await query.message.reply_text(f"❌ غلط، الإجابة الصح: *{question['a']}*", parse_mode='Markdown')
        context.user_data["score"] = score
        next_index = index + 1
        if next_index < len(QUIZ_QUESTIONS):
            await send_quiz_question(query, next_index)
        else:
            await end_quiz(query, score)
            context.user_data.clear()

    # ── معلومات البوت
    elif data == "info":
        await query.edit_message_text(
            "🤖 *معلومات البوت*\n\n"
            "بوت كلية التكنولوجيا بالفيوم.\n"
            "فيه PDFs وفيديوهات ومواقع لكل المواد.\n"
            "وبيقدم اختبار بسيط في المواد.\n\n"
            "👨‍💻 المطور: YOUSEF MAGED",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]]),
            parse_mode='Markdown'
        )

    # ── الدعم الفني
    elif data == "support":
        await query.edit_message_text(
            "📞 *الدعم الفني*\nلو عندك مشكلة كلم الإدارة 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 تواصل مع الإدارة", url=f"tg://user?id={ADMIN_ID}")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
            ]),
            parse_mode='Markdown'
        )

    # ── مشاركة البوت
    elif data == "share":
        bot_username = context.bot.username
        share_link = f"https://t.me/{bot_username}"
        await query.edit_message_text(
            f"📤 *شارك البوت مع زمايلك!*\n\n"
            f"🔗 رابط البوت:\n`{share_link}`\n\n"
            f"اضغط على الرابط وشاركه مع أي حد 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 شارك الآن", url=f"https://t.me/share/url?url={share_link}&text=بوت+كلية+التكنولوجيا+بالفيوم+للمذاكرة")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
            ]),
            parse_mode='Markdown'
        )

    # ── إحصائيات (للأدمين فقط)
    elif data == "stats" and user_id == ADMIN_ID:
        total = len(USERS)
        await query.edit_message_text(
            f"📊 *إحصائيات البوت*\n\n"
            f"👥 إجمالي المستخدمين: *{total}* مستخدم",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]]),
            parse_mode='Markdown'
        )

    # ── نشر إعلان (للأدمين فقط)
    elif data == "broadcast_mode" and user_id == ADMIN_ID:
        context.user_data["broadcast_mode"] = True
        await query.message.reply_text("✍️ اكتب الرسالة اللي عايز تنشرها لكل المستخدمين:")

# ============================================================
# إرسال الإعلان
# ============================================================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("broadcast_mode") and update.effective_user.id == ADMIN_ID:
        message = update.message.text
        count = 0
        failed = 0
        for user in USERS:
            try:
                await context.bot.send_message(chat_id=user, text=message)
                count += 1
            except:
                failed += 1
        await update.message.reply_text(
            f"📢 تم الإرسال!\n✅ وصل لـ {count} مستخدم\n❌ فشل مع {failed} مستخدم"
        )
        context.user_data["broadcast_mode"] = False

# ============================================================
# دوال الاختبار
# ============================================================
async def send_quiz_question(query, index):
    q = QUIZ_QUESTIONS[index]
    text = f"❓ *السؤال {index + 1}/{len(QUIZ_QUESTIONS)}*\n\n{q['q']}"
    await query.edit_message_text(text, reply_markup=quiz_question_kb(q["o"], index), parse_mode='Markdown')

async def end_quiz(query, score):
    total = len(QUIZ_QUESTIONS)
    percent = (score / total) * 100
    if percent == 100:
        msg = "🔥 ايوه يا دحيح! شاطر جداً"
    elif percent >= 60:
        msg = "👏 شاطر يا بشمهندس، كمّل بالجد"
    else:
        msg = "💪 حاول تحسن من مستواك المرة الجاية، إنت قادر!"
    await query.message.reply_text(
        f"🏁 *انتهى الاختبار*\n\n"
        f"📊 النتيجة: *{score}/{total}*\n"
        f"📈 النسبة: *{percent:.0f}%*\n\n{msg}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="back_main")]]),
        parse_mode='Markdown'
    )

# ============================================================
# تشغيل البوت
# ============================================================
def main():
    # شغّل السيرفر الصغير في الخلفية عشان Render يعرف البوت شغال
    threading.Thread(target=run_ping_server, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
