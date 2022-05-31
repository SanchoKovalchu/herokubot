from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot_create import cursor, connection
from keyboard import first_keyboard


class AdminRegister(StatesGroup):
    login = State()  # Will be represented in storage as 'Form:login'
    password = State()  # Will be represented in storage as 'Form:password'
    PIB = State()  # Will be represented in storage as 'Form:PIB'


async def admin_register_command(message: types.Message):
    # Set state
    await AdminRegister.login.set()
    await message.reply("Твій логін?")


async def admin_cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


async def admin_load_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await AdminRegister.next()
    await message.reply("Твій пароль?")


async def admin_load_password(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['password'] = message.text
    await AdminRegister.next()
    await message.reply("Твоє ПІБ?")


async def admin_load_PIB(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['PIB'] = message.text
        user_login = data['login']
        user_password = data['password']
        user_PIB = data['PIB']
    await state.finish()
    user_id = message.from_user.id
    sql1 = "INSERT INTO signIn_data (user_id, user_login, user_password, user_role) " \
          + " VALUES (%s, %s, %s, %s) "
    cursor.execute(sql1, (user_id, user_login, user_password, 3))
    sql2 = "INSERT INTO admin_data (user_id, PIB) " \
          + " VALUES (%s, %s) "
    cursor.execute(sql2, (user_id, user_PIB))

    connection.commit()
    await message.answer("Зареєстровано!\n"
                         "Ваші дані: \n"
                         "Логін: " + user_login + "\n"
                         "Пароль: " + user_password + "\n"
                         "ПІБ: " + user_PIB + "\n",
                         reply_markup=first_keyboard)


def register_handlers_admin_register(dp: Dispatcher):
    dp.register_message_handler(admin_register_command, lambda message: message.text == "Реєстрація адміна")
    dp.register_message_handler(admin_cancel_command, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(admin_load_login, state=AdminRegister.login)
    dp.register_message_handler(admin_load_password, state=AdminRegister.password)
    dp.register_message_handler(admin_load_PIB, state=AdminRegister.PIB)