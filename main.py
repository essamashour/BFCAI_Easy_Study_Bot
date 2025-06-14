import logging
import sys
from bot import bot
from handlers import menu  # تحميل الهاندلر
import exams_and_deadlines  
import registration  # ✅ استدعاء الملف الجديد
import utils
# إعداد ملف اللوج
logging.basicConfig(
    level=logging.DEBUG,
    filename="bot.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# تسجيل الأخطاء غير المتوقعة
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

# تشغيل البوت
if __name__ == "__main__":
    print("🚀 Bot is starting...")
    bot.run()
