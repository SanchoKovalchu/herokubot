from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

disciplines_bt = KeyboardButton('Перелік дисциплін')
marks_bt = KeyboardButton('Оцінки')
material_bt = KeyboardButton('Матеріал')
close_events_bt = KeyboardButton('Найближчі події')
tests_bt = KeyboardButton('Тестування')
settings_bt = KeyboardButton('Налаштування')


st_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

st_keyboard.add(disciplines_bt)
st_keyboard.add(marks_bt)
st_keyboard.add(close_events_bt)
st_keyboard.add(material_bt)
st_keyboard.add(tests_bt)
st_keyboard.add(settings_bt)