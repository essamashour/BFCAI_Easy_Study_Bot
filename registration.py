from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot
import sqlite3

# رجوع للقائمة الرئيسية
@bot.on_callback_query(filters.regex("^back_to_start$"))
async def back_to_start(client, callback_query):
    from handlers.menu import start_handler
    await start_handler(client, callback_query.message)

# /register
@bot.on_message(filters.command("register"))
async def start_registration(client, message):
    await choose_level_for_registration(client, message)

@bot.on_callback_query(filters.regex("^start_registration$"))
async def choose_level_for_registration(client, callback_query):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓 المستوى الأول", callback_data="reg_level_1")],
        [InlineKeyboardButton("🎓 المستوى الثاني", callback_data="reg_level_2")],
        [InlineKeyboardButton("🎓 المستوى الثالث", callback_data="reg_level_3")],
        [InlineKeyboardButton("🎓 المستوى الرابع", callback_data="reg_level_4")],
        [InlineKeyboardButton("✅ إنهاء التسجيل والرجوع", callback_data="back_to_start")]
    ])
    await callback_query.message.edit_text("📌 اختر مستواك الدراسي:", reply_markup=keyboard)

@bot.on_callback_query(filters.regex("^reg_level_\\d$"))
async def show_courses_to_register(client, callback_query):
    level = int(callback_query.data.split("_")[2])
    user_id = callback_query.from_user.id

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM courses WHERE level = ?", (level,))
    courses = cursor.fetchall()
    conn.close()

    if not courses:
        await callback_query.message.edit_text("❌ لا توجد مقررات لهذا المستوى.")
        return

    buttons = [
        [InlineKeyboardButton(f"✅ {name}", callback_data=f"select_course_{cid}")]
        for cid, name in courses
    ]
    buttons.append([
        InlineKeyboardButton("➕ مستوى آخر", callback_data="start_registration"),
        InlineKeyboardButton("💾 حفظ اختياراتي", callback_data="save_selected_courses")
    ])
    buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="start_registration")])

    await callback_query.message.edit_text("📚 اختر المقررات:", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex("^select_course_\\d+$"))
async def select_course(client, callback_query):
    user_id = callback_query.from_user.id
    course_id = int(callback_query.data.split("_")[2])

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_courses WHERE user_id = ? AND course_id = ?", (user_id, course_id))
    if cursor.fetchone():
        cursor.execute("DELETE FROM user_courses WHERE user_id = ? AND course_id = ?", (user_id, course_id))
    else:
        cursor.execute("INSERT OR IGNORE INTO user_courses (user_id, course_id) VALUES (?, ?)", (user_id, course_id))

    conn.commit()
    conn.close()
    await callback_query.answer("✅ تم تحديث اختيارك.")

@bot.on_callback_query(filters.regex("^save_selected_courses$"))
async def confirm_selection(client, callback_query):
    user_id = callback_query.from_user.id

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM courses
        JOIN user_courses ON user_courses.course_id = courses.id
        WHERE user_courses.user_id = ?
    """, (user_id,))
    selected = cursor.fetchall()
    conn.close()

    if not selected:
        await callback_query.message.edit_text("❌ لم تقم باختيار أي مقررات.")
        return

    msg = "📋 تم تسجيل المقررات التالية:\n\n"
    for (name,) in selected:
        msg += f"• {name}\n"

    msg += "\n🎉 سيتم إعلامك بأي شيء جديد يخص هذه المقررات!"
    await callback_query.message.edit_text(msg)
