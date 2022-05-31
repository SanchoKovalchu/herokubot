from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

reg_confirm_bt = KeyboardButton('Підтвердити реєстрацію')
del_user_bt = KeyboardButton('Видалити користувача')

adm_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

adm_keyboard.add(reg_confirm_bt)
adm_keyboard.add(del_user_bt)