from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

edit_all_bt = KeyboardButton('Все разом')
edit_name_bt = KeyboardButton('Назва')
edit_description_bt = KeyboardButton('Опис')
edit_file_bt = KeyboardButton('Файл')


changes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
changes_keyboard.add(edit_all_bt)
changes_keyboard.row(edit_name_bt, edit_description_bt, edit_file_bt)

add_task_bt = KeyboardButton('Додати завдання')
view_task_bt = KeyboardButton('Переглянути завдання')
back_bt = KeyboardButton("Назад")

task_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
task_keyboard.add(add_task_bt)
task_keyboard.add(view_task_bt)
task_keyboard.add(back_bt)