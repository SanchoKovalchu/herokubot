from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot_create import cursor, connection
from keyboard import first_keyboard


class TeacherRegister(StatesGroup):
    login = State()  # Will be represented in storage as 'Form:login'
    password = State()  # Will be represented in storage as 'Form:password'
    PIB = State()  # Will be represented in storage as 'Form:PIB'
    speciality = State()  # Will be represented in storage as 'Form:sp'


async def teacher_register_command(message: types.Message):
    # Set state
    await TeacherRegister.login.set()
    await message.answer("Ваш логін?")


async def teacher_cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


async def teacher_load_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await TeacherRegister.next()
    await message.answer("Ваш пароль?")


async def teacher_load_password(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['password'] = message.text
    await TeacherRegister.next()
    await message.answer("Ваше ПІБ?")


async def teacher_load_PIB(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['PIB'] = message.text
    await TeacherRegister.next()
    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("IPZ", "PP", "AND", "KN")

    await message.answer("Ваша спеціальність?", reply_markup=markup)


async def teacher_mistake_speciality(message: types.Message):
    return await message.reply("Помилка. Виберіть спеціальність із клавіатури.")


async def teacher_load_speciality(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['speciality'] = message.text
        user_login = data['login']
        user_password = data['password']
        user_PIB = data['PIB']
        speciality = data['speciality']
    await state.finish()
    user_id = message.from_user.id
    sql1 = "INSERT INTO signIn_data (user_id, user_login, user_password, user_role) " \
          + " VALUES (%s, %s, %s, %s) "
    cursor.execute(sql1, (user_id, user_login, user_password, 2))
    sql2 = "INSERT INTO teacher_data (user_id, PIB, speciality) " \
          + " VALUES (%s, %s, %s) "
    cursor.execute(sql2, (user_id, user_PIB, speciality))

    connection.commit()
    await message.answer("Зареєстровано!\n"
                         "Ваші дані: \n"
                         "Логін: " + user_login + "\n"
                         "Пароль: " + user_password + "\n"
                         "ПІБ: " + user_PIB + "\n"
                         "Кафедра: " + speciality + "\n",
                         reply_markup=first_keyboard)


def register_handlers_teacher_register(dp: Dispatcher):
    dp.register_message_handler(teacher_register_command, lambda message: message.text == "Реєстрація вчителя")
    dp.register_message_handler(teacher_cancel_command, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(teacher_load_login, state=TeacherRegister.login)
    dp.register_message_handler(teacher_load_password, state=TeacherRegister.password)
    dp.register_message_handler(teacher_load_PIB, state=TeacherRegister.PIB)
    dp.register_message_handler(teacher_mistake_speciality, lambda message: message.text not in ["IPZ", "PP", "AND", "KN"], state=TeacherRegister.speciality)
    dp.register_message_handler(teacher_load_speciality, state=TeacherRegister.speciality)