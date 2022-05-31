from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

announcement_bt = KeyboardButton('Звичайне оголошення')
poll_bt = KeyboardButton('Опитування')



ab_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

ab_keyboard.add(announcement_bt)
ab_keyboard.add(poll_bt)
