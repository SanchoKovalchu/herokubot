from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard.teacher_keyboard import tch_keyboard
from keyboard.department_keyboard import dep_keyboard, departments
from aiogram import types, Dispatcher
from bot_create import cursor, bot, connection
from datetime import datetime

from handlers.login import UserRoles

specialties = []
disciplines = []
groups = []

id = (int)

buttons = [types.KeyboardButton("Так"), types.KeyboardButton("Ні")]
bool = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True).add(*buttons)

class FSMTasks(StatesGroup):
    department = State()
    speciality = State()
    discipline = State()
    course = State()
    group = State()
    name = State()
    description = State()
    upload = State()
    time = State()
    file = State()
    student = State()

async def cm_start(message : types.Message):
    global id, groups, disciplines, specialties
    id = message.chat.id
    groups = []
    disciplines = []
    specialties = []
    await FSMTasks.department.set()
    await message.reply("На яку кафедру додати завдання?", reply_markup=dep_keyboard)

async def mistake_departments(message : types.Message):
    return await message.reply("Помилка. Оберіть кафедру з клавіатури")

async def choose_department(message : types.Message, state: FSMContext):
    global specialties
    async with state.proxy() as data:
        data["department"] = message.text
    sql = "SELECT sp_full_name AS speciality FROM study_program_list WHERE cafedra_name = %s"
    cursor.execute(sql, data["department"])
    for item in cursor.fetchall():
        specialties.append(item["speciality"])
    specialties_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    specialties_keyboard.add(*specialties)
    await message.reply("Для якої спеціальності призначено завдання?", reply_markup=specialties_keyboard)
    await FSMTasks.next()

async def mistake_specialties(message : types.Message):
    return await message.reply("Помилка. Оберіть спеціальність з клавіатури")

async def choose_speciality(message : types.Message, state : FSMContext):
    global disciplines
    async with state.proxy() as data:
        sql = "SELECT sp_abr_name AS abr FROM study_program_list WHERE sp_full_name = %s AND cafedra_name = %s"
        cursor.execute(sql,(message.text,data["department"]))
        for row in cursor:
            data["speciality"] = row["abr"]
    sql = "SELECT sb_full_name AS discipline FROM disciplines WHERE cafedra_name = %s AND speciality = %s"
    cursor.execute(sql, (data["department"], data["speciality"]))
    for item in cursor.fetchall():
        disciplines.append(item["discipline"])
    dsp_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    dsp_keyboard.add(*disciplines)
    await message.reply("Виберіть дисципліну, до якої хочете додати завдання", reply_markup=dsp_keyboard)
    await FSMTasks.next()

async def mistake_disciplines(message : types.Message):
    return await message.reply("Помилка. Оберіть дисципліну з клавіатури")

async def choose_discipline(message : types.Message, state : FSMContext):
    global disciplines
    async with state.proxy() as data:
        data["discipline"] = message.text
    course_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    course_keyboard.add("1", "2", "3", "4", "5", "6")
    await message.reply("Який курс?", reply_markup=course_keyboard)
    await FSMTasks.next()

async def mistake_course(message: types.Message):
    return await message.reply("Помилка. Оберіть курс з клавіатури")

async def choose_course(message : types.Message, state : FSMContext):
    global groups
    async with state.proxy() as data:
        data["course"] = message.text
    sql = "SELECT DISTINCT main_group FROM student_data WHERE course = %s AND sp = %s"
    cursor.execute(sql, (data["course"], data["speciality"]))
    for item in cursor.fetchall():
        groups.append(item["main_group"])
    group_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    group_keyboard.add(*groups)
    await bot.send_message(message.chat.id, "Яка група?", reply_markup=group_keyboard)
    await FSMTasks.next()

async def mistake_group(message : types.Message):
    return await message.reply("Помилка. Оберіть групу з клавіатури")

async def choose_group(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data["group"] = message.text
    await message.reply("Яка назва завдання?")
    await FSMTasks.next()

async def set_name(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await message.reply("В чому суть завдання?")
    await FSMTasks.next()

async def set_description(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
        data["date"] = datetime.now()
    await bot.send_message(message.chat.id, "Чи хочете ви додати файл?", reply_markup=bool)
    await FSMTasks.next()

async def upload_task(message : types.Message, state : FSMContext):
    if message.text == 'Так':
        await FSMTasks.file.set()
        await bot.send_message(id, "Відправте файл")
    else:
        async with state.proxy() as data:
            sql = "INSERT INTO tasks (task_name, task_description, file_id, subject_id, " \
                  "student_id, department, speciality, course, groups, deadline) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (data["name"], data["description"], None, data["discipline"], None, data["department"],
                           data["speciality"], data["course"], data["group"], data["date"]))
            connection.commit()
            await message.reply("ВСТАВЛЕНО!", reply_markup=tch_keyboard)
        await state.finish()
        await UserRoles.teacher.set()

async def upload_file(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == 'photo':
            data['file_id'] = message.photo[0].file_id
        elif message.content_type == 'video':
            data['file_id'] = message.video.file_id
        elif message.content_type == 'voice':
            data['file_id'] = message.voice.file_id
        elif message.content_type == 'audio':
            data['file_id'] = message.audio.file_id
        elif message.content_type == 'animation':
            data['file_id'] = message.animation.file_id
        elif message.content_type == 'video_note':
            data['file_id'] = message.video_note.file_id
        else:
            data['file_id'] = message.document.file_id
        data["file_id"] += ";" + str(message.content_type)
    async with state.proxy() as data:
        sql = "INSERT INTO tasks (task_name, task_description, file_id, subject_id, " \
              "student_id, department, speciality, course, groups, deadline) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (data["name"], data["description"], data["file_id"], data["discipline"], None, data["department"],
                             data["speciality"], data["course"], data["group"], data["date"]))
        connection.commit()
        await message.reply("ВСТАВЛЕНО!", reply_markup=tch_keyboard)
    await state.finish()
    await UserRoles.teacher.set()

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await UserRoles.teacher.set()
    await message.reply('Ok', reply_markup=tch_keyboard)

def register_handlers_tasks(dp : Dispatcher):
    dp.register_message_handler(cm_start, lambda message: message.text == "Додати завдання", state=UserRoles.teacher)
    dp.register_message_handler(mistake_departments, lambda message: message.text not in departments, state=FSMTasks.department)
    dp.register_message_handler(choose_department, state=FSMTasks.department)
    dp.register_message_handler(mistake_specialties, lambda message: message.text not in specialties, state=FSMTasks.speciality)
    dp.register_message_handler(choose_speciality, state=FSMTasks.speciality)
    dp.register_message_handler(mistake_disciplines, lambda message: message.text not in disciplines, state=FSMTasks.discipline)
    dp.register_message_handler(choose_discipline, state=FSMTasks.discipline)
    dp.register_message_handler(mistake_course, lambda message: message.text not in ["1", "2", "3", "4", "5", "6"], state=FSMTasks.course)
    dp.register_message_handler(choose_course, state=FSMTasks.course)
    dp.register_message_handler(mistake_group, lambda message: message.text not in groups, state=FSMTasks.group)
    dp.register_message_handler(choose_group, state=FSMTasks.group)
    dp.register_message_handler(set_name, state=FSMTasks.name)
    dp.register_message_handler(set_description, state=FSMTasks.description)
    dp.register_message_handler(upload_task, state= FSMTasks.upload)
    dp.register_message_handler(upload_file, content_types = ['photo','video','audio','document','animation','video_note','voice'], state=FSMTasks.file)
    dp.register_message_handler(cancel_handler, state="*",commands='stop')
    dp.register_message_handler(cancel_handler, Text(equals='stop', ignore_case=True), state="*")
