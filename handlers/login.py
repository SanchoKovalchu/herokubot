from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from bot_create import cursor, connection
from keyboard import st_keyboard
from keyboard import tch_keyboard


class UserRoles(StatesGroup):
    student = State()
    teacher = State()
    admin = State()

class FormLogin(StatesGroup):
    login = State()  # Will be represented in storage as 'Form:login'
    password = State()  # Will be represented in storage as 'Form:password'


async def login_command(message: types.Message):
    # Set state
    await FormLogin.login.set()
    await message.reply("Ваш логін?")


async def load_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await FormLogin.next()
    await message.reply("Ваш пароль?")


async def load_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
        login = data['login']
        password = data['password']
        await state.finish()
        sql = "SELECT * FROM signIn_data WHERE user_login = %s"
        cursor.execute(sql, login)
        #
        for row in cursor:
            user_password = row["user_password"]
            user_id = row["user_id"]
            user_role = row["user_role"]
        if user_password == password:
            # await message.answer("Ви успішно ввійшли")
            if user_role == 1:
                await UserRoles.student.set()
                sql = "SELECT * FROM student_data WHERE user_id = %s"
                cursor.execute(sql, user_id)
                for row in cursor:
                    PIB = row["PIB"]
                    sp = row["sp"]
                    course = row["course"]
                    group = row["st_group"]
                await message.answer("Вітаємо!\nВаші дані:\nПІБ: "+PIB+"\nНавчальна програма: " + sp + "\n"
                                    "Курс: "+str(course)+"\nГрупа: "+str(group), reply_markup=st_keyboard)
            elif user_role == 2:
                await UserRoles.teacher.set()
                sql = "SELECT * FROM teacher_data WHERE user_id = %s"
                cursor.execute(sql, user_id)
                for row in cursor:
                    PIB = row["PIB"]
                    speciality = row["speciality"]
                await message.answer(
                    "Вітаємо!\nВаші дані:\nПІБ: " + PIB + "\nСпеціальність: " + str(speciality), reply_markup=tch_keyboard)
            else:
                sql = "SELECT * FROM admin_data WHERE user_id = %s"
                cursor.execute(sql, user_id)
                for row in cursor:
                    PIB = row["PIB"]
                await message.answer(
                    "Вітаємо!\nВаші дані:\nПІБ: " + PIB, reply_markup=tch_keyboard)
        else:
            await message.answer("Пароль неправильний")
        connection.commit()


def register_handlers_login(dp: Dispatcher):
    dp.register_message_handler(login_command, lambda message: message.text == "Вхід")
    dp.register_message_handler(load_login, state=FormLogin.login)
    dp.register_message_handler(load_password, state=FormLogin.password)