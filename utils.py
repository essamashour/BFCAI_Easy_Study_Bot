
import sqlite3
from bot import bot

# إرسال إشعار لكل من سجل مقرر معين
async def send_announcement(course_id: int, text: str):
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    # جلب المستخدمين المسجلين في هذا المقرر
    cursor.execute("SELECT user_id FROM user_courses WHERE course_id = ?", (course_id,))
    users = cursor.fetchall()
    conn.close()

    for (user_id,) in users:
        try:
            await bot.send_message(user_id, text)
        except Exception as e:
            print(f"❌ فشل في إرسال الرسالة إلى {user_id}: {e}")
