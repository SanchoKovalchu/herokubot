from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from bot_create import cursor

sql = 'SELECT dp_full_name AS department FROM departments'
cursor.execute(sql)
departments = []
for item in cursor.fetchall():
    departments.append(item["department"])

dep_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
dep_keyboard.add(*departments)