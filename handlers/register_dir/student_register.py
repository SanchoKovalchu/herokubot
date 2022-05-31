from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot_create import cursor, connection
from keyboard import first_keyboard


class StudentRegister(StatesGroup):
    login = State()  # Will be represented in storage as 'Form:login'
    password = State()  # Will be represented in storage as 'Form:password'
    PIB = State()  # Will be represented in storage as 'Form:PIB'
    sp = State()  # Will be represented in storage as 'Form:sp'
    course = State()  # Will be represented in storage as 'Form:course'
    group = State()  # Will be represented in storage as 'Form:group'


async def student_register_command(message: types.Message):
    # Set state
    await StudentRegister.login.set()
    await message.reply("Твій логін?")


async def student_cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


async def student_load_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await StudentRegister.next()
    await message.reply("Твій пароль?")


async def student_load_password(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['password'] = message.text
    await StudentRegister.next()
    await message.reply("Твоє ПІБ?")


async def student_load_PIB(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['PIB'] = message.text
    await StudentRegister.next()
    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("IPZ", "PP", "AND", "KN")

    await message.answer("Твоя навчальна програма?", reply_markup=markup)


async def student_mistake_sp(message: types.Message):
    return await message.reply("Помилка. Оберіть навчальну програму із клавіатури")


async def student_load_sp(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['sp'] = message.text
    await StudentRegister.next()
    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("1", "2", "3", "4", "5", "6")

    await message.answer("Твій курс?", reply_markup=markup)


async def student_mistake_course(message: types.Message):
    return await message.reply("Помилка. Оберіть курс із клавіатури")


async def student_load_course(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = message.text
        await StudentRegister.next()
        # Configure ReplyKeyboardMarkup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("1", "2", "3", "4", "5")

        await message.answer("Твоя група?", reply_markup=markup)


async def student_mistake_group(message: types.Message):
    return await message.reply("Помилка. Виберіть групу із клавіатури.")


async def student_load_group(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['group'] = message.text
        user_login = data['login']
        user_password = data['password']
        PIB = data['PIB']
        sp = data['sp']
        course = data['course']
        group = data['group']
    await state.finish()
    user_id = message.from_user.id
    sql1 = "INSERT INTO signIn_data (user_id, user_login, user_password, user_role) " \
          + " VALUES (%s, %s, %s, %s) "
    cursor.execute(sql1, (user_id, user_login, user_password, 1))
    sql2 = "INSERT INTO student_data (user_id, PIB, sp, course, st_group) " \
          + " VALUES (%s, %s, %s, %s, %s) "
    cursor.execute(sql2, (user_id, PIB, sp, course, group))

    connection.commit()
    await message.answer("Зареєстровано!\n"
                         "Ваші дані: \n"
                         "Логін: " + user_login + "\n"
                         "Пароль: " + user_password + "\n"
                         "ПІБ: " + PIB + "\n"
                         "Навчальна програма: " + sp + "\n"
                         "Курс: " + course + "\n"
                         "Група: " + group,
                         reply_markup=first_keyboard)


def register_handlers_student_register(dp: Dispatcher):
    dp.register_message_handler(student_register_command, lambda message: message.text == "Реєстрація студента")
    dp.register_message_handler(student_cancel_command, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(student_load_login, state=StudentRegister.login)
    dp.register_message_handler(student_load_password, state=StudentRegister.password)
    dp.register_message_handler(student_load_PIB, state=StudentRegister.PIB)
    dp.register_message_handler(student_mistake_sp, lambda message: message.text not in ["IPZ", "PP", "AND", "KN"], state=StudentRegister.sp)
    dp.register_message_handler(student_load_sp, state=StudentRegister.sp)
    dp.register_message_handler(student_mistake_course, lambda message: message.text not in ["1", "2", "3", "4", "5", "6"], state=StudentRegister.course)
    dp.register_message_handler(student_load_course, state=StudentRegister.course)
    dp.register_message_handler(student_mistake_group, lambda message: message.text not in ["1", "2", "3", "4", "5"], state=StudentRegister.group)
    dp.register_message_handler(student_load_group, state=StudentRegister.group)