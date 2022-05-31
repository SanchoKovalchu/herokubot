from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from bot_create import cursor

sql = 'SELECT sb_full_name AS discipline FROM disciplines'
cursor.execute(sql)
disciplines = []
for item in cursor.fetchall():
    disciplines.append(item["discipline"])

dsp_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
dsp_keyboard.add(*disciplines)