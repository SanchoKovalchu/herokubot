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
class FormShowMark(StatesGroup):
    speciality = State()
    course = State()
    cathedra = State()
    group = State()
    sub_group = State()
    student = State()
    subject = State()


# mistake speciality
async def error(message: types.Message):
    return await bot.send_message(message.chat.id, "<b>Помилка. Оберіть варіант з клавіатури, будь-ласка</b>",
                                  parse_mode='HTMl')


# announcement
async def announcement_command(message: types.Message):
    # connect to database to get the specialities
    global check
    await FormShowMark.speciality.set()
    query = "SELECT DISTINCT speciality FROM disciplines"
    cursor.execute(query)

    # creating a markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for speciality in cursor.fetchall():
        markup.add(speciality["speciality"])
        check.append(speciality["speciality"])
    markup.add("Відмінити перегляд оцінок")
    check.append("Відмінити перегляд оцінок")

    # output information
    await bot.send_message(message.chat.id, text="<b>Будь-ласка, оберіть спеціальність</b>",parse_mode='HTML', reply_markup=markup)


# load speciality
async def load_speciality(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['speciality'] = message.text
    if data['speciality'] == "Відмінити перегляд оцінок":
        await bot.send_message(message.chat.id, text="<b>Повертаюсь до меню...</b>", parse_mode='HTML',
                               reply_markup=tch_keyboard)
        await state.finish()
        await UserRoles.teacher.set();
    else:
        # setting markup for courses
        await FormShowMark.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.row(str(1), str(2), str(3))
        markup.row(str(4), str(5), str(6))
        for courses in range(1, 7):
            check.append(str(courses))

        # output course
        await bot.send_message(message.chat.id, text="<b>Будь-ласка, оберіть курс</b>", parse_mode='HTML', reply_markup=markup)


async def load_course(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['course'] = message.text
    query = "SELECT DISTINCT cafedra_name FROM disciplines WHERE course = '%s' AND speciality = '%s'" % (
        data['course'], data['speciality'])
    cursor.execute(query)

    # setting markup
    await FormShowMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for cathedra in cursor.fetchall():
        markup.add(cathedra['cafedra_name'])
        check.append(cathedra['cafedra_name'])

    # output cathedra
    await bot.send_message(message.chat.id, text="<b>Будь-ласка, оберіть кафедру</b>",parse_mode='HTML', reply_markup=markup)


# load cathedra method
async def load_cathedra(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['cathedra'] = message.text
    query = "SELECT DISTINCT main_group FROM student_data WHERE course = '%s'" % (data['course'])
    cursor.execute(query)

    # setting markup
    await FormShowMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for group in cursor.fetchall():
        markup.add(group['main_group'])
        check.append(group['main_group'])

    # output subject
    await bot.send_message(message.chat.id, text="<b>Будь-ласка, оберіть групу</b>",parse_mode='HTML' ,reply_markup=markup)


# load subject
async def load_group(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['group'] = message.text
    query = "SELECT DISTINCT st_group FROM student_data WHERE course = '%s' AND main_group = '%s' " % (data['course'],
                                                                                                       data['group'])
    cursor.execute(query)

    # setting markup
    await FormShowMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for subs_group in cursor.fetchall():
        markup.add(str(subs_group['st_group']))
        check.append(str(subs_group['st_group']))

    # output group
    await bot.send_message(message.chat.id, text="<b>Будь-ласка, оберіть підгрупу</b>",parse_mode='HTML',reply_markup=markup)


# load group
async def load_sub_group(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['sub_group'] = message.text

    query = "SELECT DISTINCT PIB FROM student_data WHERE course = '%s' " \
            "AND sp = '%s' AND main_group = '%s' AND st_group = '%s'" % (data['course'], data['speciality'],
                                                                         data['group'], data['sub_group'])
    cursor.execute(query)

    # setting markup
    await FormShowMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for student in cursor.fetchall():
        markup.add(student['PIB'])
        check.append(student['PIB'])

    # output sub_group
    await bot.send_message(message.chat.id, text="<b>Будь-ласка, оберіть учня</b>",parse_mode='HTML', reply_markup=markup)


# load sub_group
async def load_student(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()

    async with state.proxy() as data:
        data['student'] = message.text

    query = "SELECT DISTINCT sb_full_name FROM disciplines WHERE cafedra_name = '%s'" % (data['cathedra'])
    cursor.execute(query)

    # setting markup
    await FormShowMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for subject in cursor.fetchall():
        markup.add(subject['sb_full_name'])
        check.append(subject['sb_full_name'])

    # output subject
    await bot.send_message(message.chat.id, text="<b>Будь-ласка, оберіть предмет</b>",parse_mode='HTML', reply_markup=markup)


# load student
async def show_marks(message: types.Message, state: FSMContext):
    # setting data
    marks_list = []
    messages = ""

    async with state.proxy() as data:
        data['subject'] = message.text

    # getting the user's id
    query = "SELECT DISTINCT user_id FROM student_data WHERE PIB = '%s'" % (data['student'])
    cursor.execute(query)
    student_id = 0
    for item in cursor.fetchall():
        student_id = int(item['user_id'])
    query = "SELECT marks_information FROM students_marks WHERE id_student = %s" % student_id
    cursor.execute(query)

    # getting the json item from db
    for item in cursor.fetchall():
        marks_list = json.loads(item['marks_information'])
    index = 1
    messages += f"<b>{data['subject']}</b>\n\n"

    # outputting information
    summary_mark = 0
    for item in marks_list:
        if item["Subject"] == data['subject']:
            messages += f'<b>{index}. {item["Comment"]}</b> \n      Оцінка за роботу : <b>{item["Mark"]}</b>\n      ' \
                        f'Вчитель, який виставив оцінку : <b>@{item["Teacher"]}</b>\n' \
                        f'      Дата виставлення : <b>{item["Date"]}</b>\n\n'
            summary_mark += float(item["Mark"])
            index = index + 1
    messages += f"<b>Сумарна оцінка за даний предмет : {summary_mark}</b>"
    await bot.send_message(message.chat.id, messages, parse_mode='HTML')

    # returning to menu

    await message.answer("<b>Повертаюсь до меню...</b>", parse_mode='HTML',
                         reply_markup=tch_keyboard)
    await state.finish()
    await UserRoles.teacher.set()


def register_handlers_marks(dp: Dispatcher):
    dp.register_message_handler(announcement_command, lambda message: message.text == "Перегляд оцінок",
                                state=UserRoles.teacher)
    dp.register_message_handler(error, lambda message: message.text not in check,
                                state=FormShowMark.speciality)
    dp.register_message_handler(load_speciality, state=FormShowMark.speciality)
    if lambda message: message.text != "Відмінити перегляд оцінок":
        dp.register_message_handler(error, lambda message: message.text not in check, state=FormShowMark.course)
        dp.register_message_handler(load_course, state=FormShowMark.course)
        dp.register_message_handler(error, lambda message: message.text not in check,
                                    state=FormShowMark.course)
        dp.register_message_handler(load_cathedra, state=FormShowMark.cathedra)
        dp.register_message_handler(error, lambda message: message.text not in check,
                                    state=FormShowMark.cathedra)
        dp.register_message_handler(load_group, state=FormShowMark.group)

        dp.register_message_handler(error, lambda message: message.text not in check, state=FormShowMark.group)
        dp.register_message_handler(load_sub_group, state=FormShowMark.sub_group)
        dp.register_message_handler(error, lambda message: message.text not in check,
                                    state=FormShowMark.sub_group)
        dp.register_message_handler(load_student, state=FormShowMark.student)
        dp.register_message_handler(error, lambda message: message.text not in check,
                                    state=FormShowMark.student)
        dp.register_message_handler(show_marks, state=FormShowMark.subject)
