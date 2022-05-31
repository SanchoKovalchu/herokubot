from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

add_material_bt = KeyboardButton('Додати матеріал')
add_additional_material_bt = KeyboardButton('Додати додатковий матеріал')
view_material_bt = KeyboardButton('Переглянути матеріал')
back_bt = KeyboardButton("Назад")



mtrl_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

mtrl_keyboard.add(add_material_bt)
mtrl_keyboard.add(add_additional_material_bt)
mtrl_keyboard.add(view_material_bt)
mtrl_keyboard.add(back_bt)