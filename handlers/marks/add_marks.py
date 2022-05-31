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
class FormAddMark(StatesGroup):
    speciality = State()
    course = State()
    cathedra = State()
    subject = State()
    group = State()
    sub_group = State()
    student = State()
    comment = State()
    mark = State()


# announcement
async def marks_start(message: types.Message):
    # connect to database to get the specialities
    global check
    markup_list = ["Додати нову оцінку", "Редагування оцінок", "Перегляд оцінок", "Назад"]
    # creating a markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)

    markup.row(markup_list[0], markup_list[1])
    markup.row(markup_list[2], markup_list[3])
    for item in markup_list:
        check.append(item)
    await bot.send_message(message.chat.id, text="<b>Оберіть пункт меню роботи з оцінками:</b>", parse_mode='HTML',
                           reply_markup=markup)


# mistake speciality
async def error(message: types.Message):
    return await bot.send_message(message.chat.id, "<b>Помилка. Оберіть варіант з клавіатури, будь-ласка</b>",
                                  parse_mode='HTMl')


# announcement
async def announcement_command(message: types.Message):
    # connect to database to get the specialities
    global check
    await FormAddMark.speciality.set()
    query = "SELECT DISTINCT speciality FROM disciplines"
    cursor.execute(query)

    # creating a markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for speciality in cursor.fetchall():
        markup.add(speciality["speciality"])
        check.append(speciality["speciality"])
    markup.add("Відмінити надання оцінок")
    check.append("Відмінити надання оцінок")

    # output information
    await bot.send_message(message.chat.id, text="Оберіть спеціальність", reply_markup=markup)



# load speciality
async def load_speciality(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['speciality'] = message.text
    if (data['speciality'] == "Відмінити надання оцінок"):
        await bot.send_message(message.chat.id, text="<b>Повертаюсь до меню...</b>", parse_mode='HTML',
                               reply_markup=tch_keyboard)
        await state.finish()
        await UserRoles.teacher.set();
    else:
        # setting markup for courses
        await FormAddMark.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.row(str(1), str(2), str(3))
        markup.row(str(4), str(5), str(6))
        for courses in range(1, 7):
            check.append(str(courses))

        # output course
        await bot.send_message(message.chat.id, text="Оберіть курс", reply_markup=markup)



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
    await FormAddMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for cathedra in cursor.fetchall():
        markup.add(cathedra['cafedra_name'])
        check.append(cathedra['cafedra_name'])

    # output cathedra
    await bot.send_message(message.chat.id, text="Оберіть кафедру", reply_markup=markup)



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
    await FormAddMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for subject in cursor.fetchall():
        markup.add(subject['sb_full_name'])
        check.append(subject['sb_full_name'])

    # output subject
    await bot.send_message(message.chat.id, text="Оберіть предмет", reply_markup=markup)



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
    await FormAddMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for group in cursor.fetchall():
        markup.add(str(group['main_group']))
        check.append(str(group['main_group']))

    # output group
    await bot.send_message(message.chat.id, text="Оберіть групу", reply_markup=markup)



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
    await FormAddMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for subs_group in cursor.fetchall():
        markup.add(str(subs_group['st_group']))
        check.append(str(subs_group['st_group']))

    # output sub_group
    await bot.send_message(message.chat.id, text="Оберіть підгрупу", reply_markup=markup)



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
    await FormAddMark.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for student in cursor.fetchall():
        markup.add(student['PIB'])
        check.append(student['PIB'])

    # output sub_group
    await bot.send_message(message.chat.id, text="Оберіть учня", reply_markup=markup)


# load student
async def load_student(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['student'] = message.text
    await FormAddMark.next()
    await bot.send_message(message.chat.id, text="Напишіть назву роботи, за яку виставляється оцінка",
                           reply_markup=types.ReplyKeyboardRemove())


# load comment
async def load_comment(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()
    async with state.proxy() as data:
        data['comment'] = message.text
    await FormAddMark.next()
    await bot.send_message(message.chat.id, "Поставте оцінку користувачу")


# load student
async def load_mark(message: types.Message, state: FSMContext):
    # setting data
    global check
    check.clear()

    # variables
    date = datetime.date.today()
    username = message.chat.username

    async with state.proxy() as data:
        data['mark'] = message.text

    query = "SELECT DISTINCT user_id FROM student_data WHERE PIB = '%s'" % (data['student'])
    cursor.execute(query)
    student_id = 0
    for item in cursor.fetchall():
        student_id = int(item['user_id'])

    # checking if the user have already any marks
    query = "SELECT marks_information FROM students_marks WHERE id_student = '%s'" % student_id
    cursor.execute(query)
    marks = cursor.fetchall()

    # if it's the first user's mark
    if not marks:
        students = [
            {"PIB": data['student'], "Subject": data['subject'], "Mark": data['mark'], "Comment": data['comment'],
             "Date": str(date), "Teacher": username}]
        students_json = json.dumps(students)
        query = "INSERT INTO students_marks (id_student, marks_information) VALUES (%s, %s)"
        cursor.execute(query, (student_id, students_json))
        connection.commit()

    # if user already has some marks
    else:
        query = "SELECT marks_information FROM students_marks WHERE id_student = '%s'" % student_id
        cursor.execute(query)
        for item in cursor.fetchall():
            marks_get = json.loads(item['marks_information'])

        students = {"PIB": data['student'], "Subject": data['subject'], "Mark": data['mark'],
                    "Comment": data['comment'],
                    "Date": str(date), "Teacher": username}
        marks_get.append(students)
        marks_get = json.dumps(marks_get)

        # update db
        query = "UPDATE students_marks SET marks_information = %s WHERE id_student = %s"
        cursor.execute(query, (marks_get, student_id))
        connection.commit()

    await message.answer("Оцінка була виставлена", reply_markup=tch_keyboard)
    await state.finish()
    await UserRoles.teacher.set()


def register_handlers_marks(dp: Dispatcher):
    dp.register_message_handler(marks_start, lambda message: message.text == "Робота з Оцінками",
                                state=UserRoles.teacher)
    dp.register_message_handler(announcement_command, lambda message: message.text == "Додати нову оцінку",
                                state=UserRoles.teacher)
    dp.register_message_handler(error, lambda message: message.text not in check,
                                state=FormAddMark.speciality)
    dp.register_message_handler(load_speciality, state=FormAddMark.speciality)
    if lambda message: message.text != "Відмінити надання оцінок":
        dp.register_message_handler(error, lambda message: message.text not in check, state=FormAddMark.course)
        dp.register_message_handler(load_course, state=FormAddMark.course)
        dp.register_message_handler(error, lambda message: message.text not in check,
                                    state=FormAddMark.cathedra)
        dp.register_message_handler(load_cathedra, state=FormAddMark.cathedra)
        dp.register_message_handler(error, lambda message: message.text not in check,
                                    state=FormAddMark.subject)
        dp.register_message_handler(load_subject, state=FormAddMark.subject)
        dp.register_message_handler(error, lambda message: message.text not in check, state=FormAddMark.group)
        dp.register_message_handler(load_group, state=FormAddMark.group)
        dp.register_message_handler(error, lambda message: message.text not in check,
                                    state=FormAddMark.sub_group)
        dp.register_message_handler(load_sub_group, state=FormAddMark.sub_group)
        dp.register_message_handler(error, lambda message: message.text not in check,
                                    state=FormAddMark.student)
        dp.register_message_handler(load_student, state=FormAddMark.student)
        dp.register_message_handler(load_comment, state=FormAddMark.comment)
        dp.register_message_handler(load_mark, state=FormAddMark.mark)
