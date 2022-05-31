from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

login_bt = KeyboardButton('Вхід')
register_st_bt = KeyboardButton('Реєстрація студента')
register_tch_bt = KeyboardButton('Реєстрація вчителя')
register_adm_bt = KeyboardButton('Реєстрація адміна')


first_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
first_keyboard.add(login_bt)
first_keyboard.add( register_st_bt, register_tch_bt, register_adm_bt)
