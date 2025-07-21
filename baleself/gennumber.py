import requests
import random
import sqlite3  # ۱. کتابخانه sqlite3 را وارد می‌کنیم که برای کار با دیتابیس استفاده می‌شود.

def create_database(db_name):  # ۲. تابعی برای ایجاد دیتابیس تعریف می‌کنیم. نام دیتابیس به عنوان ورودی دریافت می‌شود.
    conn = sqlite3.connect(db_name)  # ۳. اتصال به دیتابیس با استفاده از نام دیتابیس. اگر دیتابیس وجود نداشته باشد، ایجاد می‌شود.
    cursor = conn.cursor()  # ۴. یک شی cursor برای اجرای دستورات SQL ایجاد می‌کنیم.

    # ۵. ایجاد یک جدول به نام users با دو فیلد username و password
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')  
    conn.commit()  # ۶. تغییرات را در دیتابیس ذخیره می‌کنیم.
    conn.close()  # ۷. اتصال به دیتابیس را می‌بندیم.

def insert_user(db_name, username, password):  # ۸. تابعی برای درج یک کاربر جدید تعریف می‌کنیم.
    conn = sqlite3.connect(db_name)  # ۹. اتصال به دیتابیس
    cursor = conn.cursor()  # ۱۰. ایجاد یک شی cursor
    
    # ۱۱. دستور SQL برای درج کاربر جدید
    cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, password))  # ۱۲. استفاده از جایگزینی برای جلوگیری از حملات SQL Injection
    
    conn.commit()  # ۱۳. تغییرات را ذخیره می‌کنیم.
    conn.close()  # ۱۴. اتصال را می‌بندیم.

def delete_user(db_name, username):  # ۱۵. تابعی برای حذف یک کاربر بر اساس نام کاربری تعریف می‌کنیم.
    conn = sqlite3.connect(db_name)  # ۱۶. اتصال به دیتابیس
    cursor = conn.cursor()  # ۱۷. ایجاد یک شی cursor
    
    # ۱۸. دستور SQL برای حذف کاربر بر اساس نام کاربری
    cursor.execute('''
        DELETE FROM users WHERE username = ?
    ''', (username,))  # ۱۹. استفاده از جایگزینی برای جلوگیری از حملات SQL Injection
    
    conn.commit()  # ۲۰. تغییرات را ذخیره می‌کنیم.
    conn.close()  # ۲۱. اتصال را می‌بندیم.

create_database('users.db')  # ۲۲. دیتابیس را ایجاد می‌کنیم.

def user_exists(db_name, username):  # ۲۲. تابعی برای بررسی وجود کاربر بر اساس نام کاربری
    conn = sqlite3.connect(db_name)  # ۲۳. اتصال به دیتابیس
    cursor = conn.cursor()  # ۲۴. ایجاد یک شی cursor

    # ۲۵. دستور SQL برای بررسی وجود کاربر
    cursor.execute('''
    SELECT * FROM users WHERE username = ?
    ''', (username,))  # ۲۶. استفاده از جایگزینی برای جلوگیری از حملات SQL Injection

    user = cursor.fetchone()  # ۲۷. دریافت یک رکورد (اگر وجود داشته باشد)
    conn.close()  # ۲۸. اتصال را می‌بندیم

    return user is not None  # ۲۹. بازگرداندن True اگر کاربر وجود داشته باشد و False در غیر این صورت


def select_password(db_name, username): # ۱۵. تابعی برای انتخاب پسورد با نام کاربری ورودی.
    conn = sqlite3.connect(db_name) # ۱۶. اتصال به دیتابیس
    cursor = conn.cursor() # ۱۷. ایجاد یک شی cursor
    
    # ۱۸. دستور SQL برای انتخاب پسورد بر اساس نام کاربری
    cursor.execute('''
    SELECT password FROM users WHERE username = ?
    ''', (username,)) # ۱۹. استفاده از پارامترهای جایگزین
    
    password = cursor.fetchone() # ۲۰. دریافت یک رکورد (پسورد) از نتایج
    conn.close() # ۲۱. بستن اتصال

    return password[0] if password else None # ۲۲. بازگرداندن پسورد یا None اگر کاربر پیدا نشود.

def generate_hamrah_avval():
    # پیش‌شماره‌های معتبر همراه اول
    prefixes = ['0910', '0911', '0912', '0913', '0914', '0915', '0916', '0917', '0918', '0919']
    prefix = random.choice(prefixes)
    number = ''.join(random.choices('0123456789', k=7))
    return prefix + number

def generate_irancell():
    # پیش‌شماره‌های معتبر ایرانسل
    prefixes = ['0930', '0933', '0935', '0936', '0937', '0938', '0939']
    prefix = random.choice(prefixes)
    number = ''.join(random.choices('0123456789', k=7))
    return prefix + number

def get_user_id(number):
    response = requests.get(f"https://api.daradege.ir/bale_id_data?username=@{number}")
    if str(response.json()["status"] == "success"):
        # بله دارد
        if user_exists("numbers.db",str(response.json()["user_id"])):
            return "exists!"
        else:
            insert_user("numbers.db",str(response.json()["user_id"]),number)
            return str(response.json()["user_id"])
    else:
        # بله ندارد
        return False
create_database("numbers.db")
# for i in range(1,10):
# get_user_id(generate_hamrah_avval())
# get_user_id(generate_irancell())

print(get_user_id("09044395749"))