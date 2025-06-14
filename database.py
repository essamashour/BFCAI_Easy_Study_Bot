import sqlite3

def create_tables():
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    print("📦 جاري إنشاء الجداول...")

    # جدول المقررات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        level INTEGER NOT NULL,
        term INTEGER NOT NULL,
        has_sections INTEGER DEFAULT 0
    )
    """)

    # جدول المستخدمين
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        registered_courses TEXT
    )
    """)

    # جدول المحاضرات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lectures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        file_path TEXT NOT NULL,
        FOREIGN KEY(course_id) REFERENCES courses(id)
    )
    """)

    # جدول السكاشن
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        file_path TEXT NOT NULL,
        FOREIGN KEY(course_id) REFERENCES courses(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ تم إنشاء قاعدة البيانات والجداول بنجاح.")

def insert_sample_courses():
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    courses = [
        ("رياضة 1", 1, 1, 0),
        ("برمجة 1", 1, 1, 1),  # هذا له سكاشن
        ("مقدمة في الحاسب", 1, 1, 0),
        ("رياضة منطقية", 1, 1, 0),
        ("برمجة 2", 1, 2, 1),
        ("هياكل بيانات", 1, 2, 1),
        ("قواعد بيانات", 1, 2, 0),
        ("إحصاء", 1, 2, 0),
        ("شبكات", 2, 1, 1),
        ("نظم تشغيل", 2, 1, 0)
    ]

    cursor.executemany("INSERT INTO courses (name, level, term, has_sections) VALUES (?, ?, ?, ?)", courses)
    conn.commit()
    conn.close()
    print("✅ تم إدخال المقررات بنجاح.")

def insert_sample_content():
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    lectures = [
        (2, "Lecture 1", "files/lec1.pdf"),
        (2, "Lecture 2", "files/lec2.pdf"),
        (2, "Lecture 3", "files/lec3.pdf")
    ]

    sections = [
        (2, "Section 1", "files/sec1.pdf"),
        (2, "Section 2", "files/sec2.pdf")
    ]

    cursor.executemany("INSERT INTO lectures (course_id, title, file_path) VALUES (?, ?, ?)", lectures)
    cursor.executemany("INSERT INTO sections (course_id, title, file_path) VALUES (?, ?, ?)", sections)

    conn.commit()
    conn.close()
    print("✅ تم إدخال المحاضرات والسكاشن بنجاح.")

# تشغيل الوظائف
if __name__ == "__main__":
    create_tables()
    insert_sample_courses()
    insert_sample_content()
