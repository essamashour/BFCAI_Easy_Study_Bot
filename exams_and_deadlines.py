
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot
import sqlite3
import os

# ✅ عرض أنواع الامتحانات داخل المقرر
@bot.on_callback_query(filters.regex("^exams_\d+$"))
async def show_exam_types(client, callback_query):
    course_id = int(callback_query.data.split("_")[1])

    buttons = [
        [InlineKeyboardButton("📝 ميدترم", callback_data=f"examtype_mid_{course_id}")],
        [InlineKeyboardButton("🎯 فاينال", callback_data=f"examtype_final_{course_id}")],
        [InlineKeyboardButton("❓ كويزات", callback_data=f"examtype_quiz_{course_id}")],
        [InlineKeyboardButton("🧪 عملي", callback_data=f"examtype_lab_{course_id}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"course_{course_id}")]
    ]

    await callback_query.message.edit_text(
        "اختر نوع الامتحان لعرض الملفات:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ إرسال صور امتحانات من مجلدات منظمة مثل exams/mid/course_1/
@bot.on_callback_query(filters.regex("^examtype_(mid|final|quiz|lab)_\d+$"))
async def send_exam_images(client, callback_query):
    parts = callback_query.data.split("_")
    exam_type = parts[1]  # mid أو final أو quiz أو lab
    course_id = int(parts[2])

    folder = f"exams/{exam_type}/course_{course_id}"
    if not os.path.exists(folder):
        await callback_query.message.reply_text("❌ لا توجد صور لهذا النوع.")
        return

    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".png"))]
    if not files:
        await callback_query.message.reply_text("❌ لا توجد صور داخل المجلد.")
        return

    for image in files:
        path = os.path.join(folder, image)
        await callback_query.message.reply_photo(photo=path)

# ✅ عرض المواعيد المهمة داخل المقرر
@bot.on_callback_query(filters.regex("^deadlines_\d+$"))
async def show_deadlines(client, callback_query):
    course_id = int(callback_query.data.split("_")[1])

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, due_date FROM deadlines WHERE course_id = ?", (course_id,))
    items = cursor.fetchall()
    conn.close()

    if not items:
        await callback_query.message.edit_text("❌ لا توجد مواعيد مهمة مسجلة.")
        return

    text = "⏰ <b>المواعيد المهمة:</b>\n\n"
    for title, due in items:
        text += f"• <b>{title}</b>: {due}\n"

    text += "\n🔙 رجوع"
    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data=f"course_{course_id}")]
        ]),
        parse_mode="HTML"
    )
