from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from handlers.login import UserRoles
from keyboard.teacher_keyboard import tch_keyboard
from aiogram.dispatcher.filters import Text
from bot_create import connection, cursor, bot
from datetime import datetime


class FormPoll(StatesGroup):
    course = State()
    groups = State()
    question = State()
    poll = State()


async def cm_start_(message: types.Message):
    await FormPoll.course.set()
    await bot.send_message(message.chat.id, "Введіть курси, які повинні отримати повідомлення \nПриклад: 1, 2, 3")


async def choose_courses(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = message.text
    await FormPoll.next()
    await message.reply("Введіть групи, які повинні отримати повідомлення \nПриклад: 1, 2, 3")


async def choose_groups(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await FormPoll.next()
    await bot.send_message(message.chat.id, "Введіть запитання опитування")


async def select_question(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await FormPoll.next()
    await bot.send_message(message.chat.id, "Введіть опції опитування \nПриклад: Так, Ні, Не знаю")


async def create_poll(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['option'] = message.text
        option = data['option']
        options = option.split(", ")
        group = data['group']
        groups = group.split(", ")
        course = data['course']
        courses = course.split(", ")
        question = data['question']
    sql = "SELECT * FROM student_data"
    cursor.execute(sql)
    user_id_array = []
    course_id_array = []
    user_group_array = []

    i = -1
    for row in cursor:
        i += 1
        user_id_array.append(row["user_id"])
        course_id_array.append(row["course"])
        user_group_array.append(row["st_group"])
    await message.answer_poll(
                        question=question,
                        options=options,
                        type='regular',
                        correct_option_id=0,
                        is_anonymous=False)
    async with state.proxy() as data:
        data['message_id'] = message.message_id+1
    for i in range(len(course_id_array)):
        for ii in range(len(courses)):
            for iii in range(len(groups)):
                if str(course_id_array[i]) == courses[ii]:
                    if str(user_group_array[i]) == groups[iii]:
                        try:
                            await bot.forward_message(user_id_array[i], message.chat.id, message.message_id+1)
                        except:
                            print(user_id_array[i], " User not found")
    await bot.send_message(message.chat.id, "Створено!", reply_markup=tch_keyboard)

    async with state.proxy() as data:
        sql = "INSERT INTO poll_storage(chat_id, message_id, datetime) " \
        + " VALUES (%s, %s, %s) "
        chat_id = message.chat.id
        message_id = data['message_id']
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%y %H:%M:%S")
        cursor.execute(sql, (chat_id, message_id, dt_string))
        connection.commit()

    await state.finish()
    await UserRoles.teacher.set()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await UserRoles.teacher.set()
    await message.reply('Ok', reply_markup=tch_keyboard)


def register_handlers_poll_announcement(dp: Dispatcher):
    dp.register_message_handler(cm_start_, lambda message: message.text == "Створити нове опитування", state=UserRoles.teacher)
    dp.register_message_handler(choose_courses, state=FormPoll.course)
    dp.register_message_handler(choose_groups, state=FormPoll.groups)
    dp.register_message_handler(select_question, state=FormPoll.question)
    dp.register_message_handler(create_poll, state=FormPoll.poll)
    dp.register_message_handler(cancel_handler, state="*", commands='stop')
    dp.register_message_handler(cancel_handler, Text(equals='stop', ignore_case=True), state="*")
