from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

new_poll_bt = KeyboardButton('Створити нове опитування')
view_poll_bt = KeyboardButton('Переглянути опитування')



pb_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

pb_keyboard.add(new_poll_bt)
pb_keyboard.add(view_poll_bt)