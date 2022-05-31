import json
import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_create import cursor, bot, connection
from handlers.login import UserRoles
from keyboard.teacher_keyboard import tch_keyboard

# item to check
check = []


# state
class FormEditMark(StatesGroup):
    speciality = State()
    course = State()
    cathedra = State()
    subject = State()
    group = State()
    sub_group = State()
    student = State()
    change = State()


# announcement
async def announcement_command(message: types.Message):
    # connect to database to get the specialities
    global check
    await FormEditMark.speciality.set()
    query = "SELECT DISTINCT speciality FROM disciplines"
    cursor.execute(query)

    # creating a markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for speciality in cursor.fetchall():
        markup.add(speciality["speciality"])
        check.append(speciality["speciality"])
    markup.add("Відмінити редагування оцінок")
    check.append("Відмінити редагування оцінок")

    # output information
    await bot.send_message(message.chat.id, text="Оберіть спеціальність", reply_markup=markup)


# mistake speciality
async def mistake_speciality(message: types.Message):
    return await bot.send_message(message.chat.id, "Помилка. Оберіть спеціальність із клавіатури")


# load speciality
async def load_speciality(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['speciality'] = message.text
    if (data['speciality'] == "Відмінити редагування оцінок"):
        await bot.send_message(message.chat.id, text="<b>Повертаюсь до меню...</b>", parse_mode='HTML',
                               reply_markup=tch_keyboard)
        await state.finish()
        await UserRoles.teacher.set();
    else:
        # setting markup for courses
        await FormEditMark.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        for courses in range(1, 7):
            check.append(str(courses))
            markup.add(str(courses))

        # output course
        await bot.send_message(message.chat.id, text="Оберіть курс", reply_markup=markup)


# mistake course
async def mistake_course(message: types.Message):
    return await bot.send_message(message.chat.id, "Помилка. Оберіть курс із клавіатури")


async def load_course(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['course'] = message.text
    query = "SELECT DISTINCT cafedra_name FROM disciplines WHERE course = '%s' AND speciality = '%s'" % (data['course'],
                                                                                                         data['speciality'])
    cursor.execute(query)

    # setting markup
    await FormEditMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for cathedra in cursor.fetchall():
        markup.add(cathedra['cafedra_name'])
        check.append(cathedra['cafedra_name'])

    # output cathedra
    await bot.send_message(message.chat.id, text="Оберіть кафедру", reply_markup=markup)


# mistake cathedra
async def mistake_cathedra(message: types.Message):
    return await bot.send_message(message.chat.id, "Помилка. Оберіть кафедру із клавіатури")


# load cathedra method
async def load_cathedra(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['cathedra'] = message.text
    query = "SELECT DISTINCT sb_full_name FROM disciplines WHERE cafedra_name = '%s'" % (data['cathedra'])
    cursor.execute(query)

    # setting markup
    await FormEditMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for subject in cursor.fetchall():
        markup.add(subject['sb_full_name'])
        check.append(subject['sb_full_name'])

    # output subject
    await bot.send_message(message.chat.id, text="Оберіть предмет", reply_markup=markup)


# mistake subject
async def mistake_subject(message: types.Message):
    return await bot.send_message(message.chat.id, "Помилка. Оберіть предмет із клавіатури")


# load subject
async def load_subject(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['subject'] = message.text
    query = "SELECT DISTINCT main_group FROM student_data WHERE course = '%s'" % (data['course'])
    cursor.execute(query)

    # setting markup
    await FormEditMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for group in cursor.fetchall():
        markup.add(str(group['main_group']))
        check.append(str(group['main_group']))

    # output group
    await bot.send_message(message.chat.id, text="Оберіть групу", reply_markup=markup)


# mistake group
async def mistake_group(message: types.Message):
    return await bot.send_message(message.chat.id, "Помилка. Оберіть групу із клавіатури")


# load group
async def load_group(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['group'] = message.text
    query = "SELECT DISTINCT st_group FROM student_data WHERE main_group = '%s'" % (data['group'])
    cursor.execute(query)

    # setting markup
    await FormEditMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for subs_group in cursor.fetchall():
        markup.add(str(subs_group['st_group']))
        check.append(str(subs_group['st_group']))

    # output sub_group
    await bot.send_message(message.chat.id, text="Оберіть підгрупу", reply_markup=markup)


# mistake sub_group
async def mistake_sub_group(message: types.Message):
    return await bot.send_message(message.chat.id, "Помилка. Оберіть підгрупу із клавіатури")


# load sub_group
async def load_sub_group(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['sub_group'] = message.text
    query = "SELECT DISTINCT PIB FROM student_data WHERE course = '%s' AND sp = '%s' AND main_group = '%s' AND st_group = '%s'" % (
    data['course'], data['speciality'], data['group'], data['sub_group'])
    cursor.execute(query)

    # setting markup
    await FormEditMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for student in cursor.fetchall():
        markup.add(student['PIB'])
        check.append(student['PIB'])

    # output sub_group
    await bot.send_message(message.chat.id, text="Оберіть учня", reply_markup=markup)


# mistake student
async def mistake_student(message: types.Message):
    return await bot.send_message(message.chat.id, "Помилка. Оберіть студента із клавіатури")


# load student
async def load_student(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['student'] = message.text
    await FormEditMark.next()
    await bot.send_message(message.chat.id, text="Напишіть назву роботи, за яку виставляється оцінка",
                           reply_markup=types.ReplyKeyboardRemove())


def register_handlers_marks(dp: Dispatcher):
    dp.register_message_handler(announcement_command, lambda message: message.text == "Редагування оцінок",
                                state=UserRoles.teacher)
    dp.register_message_handler(mistake_speciality, lambda message: message.text not in check,
                                state=FormEditMark.speciality)
    dp.register_message_handler(load_speciality, state=FormEditMark.speciality)
    if lambda message: message.text != "Відмінити редагування оцінок":
        dp.register_message_handler(mistake_course, lambda message: message.text not in check,
                                    state=FormEditMark.course)
        dp.register_message_handler(load_course, state=FormEditMark.course)
        dp.register_message_handler(mistake_cathedra, lambda message: message.text not in check,
                                    state=FormEditMark.cathedra)
        dp.register_message_handler(load_cathedra, state=FormEditMark.cathedra)
        dp.register_message_handler(mistake_subject, lambda message: message.text not in check,
                                    state=FormEditMark.subject)
        dp.register_message_handler(load_subject, state=FormEditMark.subject)
        dp.register_message_handler(mistake_group, lambda message: message.text not in check, state=FormEditMark.group)
        dp.register_message_handler(load_group, state=FormEditMark.group)
        dp.register_message_handler(mistake_sub_group, lambda message: message.text not in check,
                                    state=FormEditMark.sub_group)
        dp.register_message_handler(load_sub_group, state=FormEditMark.sub_group)
        dp.register_message_handler(mistake_student, lambda message: message.text not in check,
                                    state=FormEditMark.student)
        dp.register_message_handler(load_student, state=FormEditMark.student)
