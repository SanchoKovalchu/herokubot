from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

edit_all_bt = KeyboardButton('Все разом')
edit_name_bt = KeyboardButton('Назва')
edit_description_bt = KeyboardButton('Опис')
edit_subject_bt = KeyboardButton('Предмет')


fl_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
fl_keyboard.add(edit_all_bt)
fl_keyboard.add(edit_name_bt, edit_description_bt, edit_subject_bt)