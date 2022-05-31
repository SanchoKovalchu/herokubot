from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

disciplines_bt = KeyboardButton('Перелік дисциплін')
groups_bt = KeyboardButton('Групи студентів')
announcement_bt = KeyboardButton('Оголошення')
material_bt = KeyboardButton('Матеріал')
tasks_bt = KeyboardButton("Завдання")
marks_bt = KeyboardButton('Робота з Оцінками')
tests_bt = KeyboardButton('Створити тест')
settings_bt = KeyboardButton('Налаштування')


tch_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

tch_keyboard.add(disciplines_bt)
tch_keyboard.add(groups_bt)
tch_keyboard.add(announcement_bt)
tch_keyboard.add(material_bt)
tch_keyboard.add(tasks_bt)
tch_keyboard.add(marks_bt)
tch_keyboard.add(tests_bt)
tch_keyboard.add(settings_bt)