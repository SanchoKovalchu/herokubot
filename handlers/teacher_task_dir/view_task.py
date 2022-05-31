#bot & fsm
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_create import cursor, bot
from aiogram import types, Dispatcher
#keyboards
from keyboard.teacher_keyboard import tch_keyboard
from keyboard.department_keyboard import dep_keyboard, departments

#additional info
from handlers.teacher_task_dir.delete_task import cm_start_delete
from handlers.teacher_task_dir.edit_task import cm_start_edit

from aiogram.dispatcher.filters import Text
from datetime import datetime

from handlers.login import UserRoles

specialties = []
groups = []

msg = (str)
id = (int)

class FSMViewTasks(StatesGroup):
    department = State()
    speciality = State()
    course = State()
    group = State()

async def cm_start(message: types.Message):
    global id
    global specialties
    global groups
    specialties = []
    groups = []
    id = message.chat.id
    await FSMViewTasks.department.set()
    await bot.send_message(message.chat.id, "Оберіть кафедру, завдання якої хочете побачити", reply_markup=dep_keyboard)

async def mistake_departments(message : types.Message):
    return await message.reply("Помилка. Оберіть кафедру з клавіатури")

async def choose_department(message : types.Message, state : FSMContext):
    global specialties
    async with state.proxy() as data:
        data["department"] = message.text
    sql = "SELECT sp_full_name AS speciality FROM study_program_list WHERE cafedra_name = %s"
    cursor.execute(sql, data["department"])
    for item in cursor.fetchall():
        specialties.append(item["speciality"])
    specialties_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    specialties_keyboard.add(*specialties)
    await message.reply("Оберіть спеціальність", reply_markup=specialties_keyboard)
    await FSMViewTasks.next()

async def mistake_specialties(message : types.Message):
    return await message.reply("Помилка. Оберіть спеціальність з клавіатури")

async def choose_speciality(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        sql = "SELECT sp_abr_name AS abr FROM study_program_list WHERE sp_full_name = %s AND cafedra_name = %s"
        cursor.execute(sql, (message.text, data["department"]))
        for row in cursor:
            data["speciality"] = row["abr"]
        sql = "SELECT subject FROM teacher_data WHERE user_id = %s"
        cursor.execute(sql, message.chat.id)
        for row in cursor:
            data["subject"] = row["subject"]
    course_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    course_keyboard.add("1", "2", "3", "4", "5", "6")
    await message.reply("Оберіть курс", reply_markup=course_keyboard)
    await FSMViewTasks.next()

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
    await message.reply("Яка група?", reply_markup=group_keyboard)
    await FSMViewTasks.next()

async def mistake_group(message : types.Message):
    return await message.reply("Помилка. Оберіть групу з клавіатури")

async def choose_group(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data["group"] = message.text
    await show_tasks(state)

def get_keyboard(data: str):
    callback_data_check = str(data) + '_check'
    callback_data_edit = str(data) + '_editTask'
    callback_data_delete = str(data) + '_deleteTask'
    button_check = types.InlineKeyboardButton(text="Переглянути відповіді студентів", callback_data=callback_data_check)
    button_edit = types.InlineKeyboardButton(text="Редагувати", callback_data=callback_data_edit)
    button_delete = types.InlineKeyboardButton(text="Видалити", callback_data=callback_data_delete)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(button_check)
    keyboard.row(button_edit, button_delete)
    return keyboard

async def show_tasks(state : FSMContext):
    global id
    global msg
    await bot.send_message(id, "<b>Завдання</b>", reply_markup=tch_keyboard, parse_mode='HTML')
    async with state.proxy() as data:
        sql = "SELECT * FROM tasks WHERE department=%s and speciality=%s and course=%s and groups=%s"
        cursor.execute(sql, (data["department"], data["speciality"], data["course"], data["group"]))
    for row in cursor.fetchall():
        message_text = f'<b>{row["task_name"]}</b>\n' \
              f'...............................................................\n' \
              f'{row["task_description"]}\n' \
              f'...............................................................\n' \
              f'<b>Дедлайн</b>: <u>{str(row["deadline"])}</u>\n' \
              f'<i>До кінця здачі залишилось: {row["deadline"] - datetime.now()}</i>\n' \
              f'...............................................................\n'
        if row["file_id"] == None:
            msg = await bot.send_message(id, message_text,reply_markup=get_keyboard(row["id"]), parse_mode='html')
        else:
            file_id = str(row["file_id"].split(sep=";")[0])
            file_type = str(row["file_id"].split(sep=";")[1])
            match file_type:
                case 'photo':
                    msg = await bot.send_photo(chat_id=id, photo=file_id, caption=message_text,
                                         reply_markup=get_keyboard(row["id"]), parse_mode='html')
                case 'video':
                    msg = await bot.send_video(chat_id=id, video=file_id, caption=message_text,
                                         reply_markup=get_keyboard(row["id"]), parse_mode='html')
                case 'audio':
                    msg = await bot.send_audio(chat_id=id, audio=file_id, caption=message_text,
                                         reply_markup=get_keyboard(row["id"]), parse_mode='html')
                case 'voice':
                    msg = await bot.send_voice(chat_id=id, voice=file_id, caption=message_text,
                                         reply_markup=get_keyboard(row["id"]), parse_mode='html')
                case 'animation':
                    msg = await bot.send_animation(chat_id=id, animation=file_id, caption=message_text,
                                             reply_markup=get_keyboard(row["id"]), parse_mode='html')
                case 'video_note':
                    msg = await bot.send_video_note(chat_id=id, video_note=file_id, caption=message_text,
                                              reply_markup=get_keyboard(row["id"]), parse_mode='html')
                case _:
                    msg = await bot.send_document(chat_id=id, document=file_id, caption=message_text,
                                            reply_markup=get_keyboard(row["id"]), parse_mode='html')
    await state.finish()
    await UserRoles.teacher.set()

async def callback_command(call: types.CallbackQuery):
    global msg
    command = call.data.split(sep="_")[1]
    if command == "check":
        await cm_start_check(call.data,call.from_user.id)
    elif command == "deleteTask":
        await cm_start_delete(call.data,call.from_user.id, msg)
    else:
        await cm_start_edit(call.data,call.from_user.id, msg)

async def cm_start_check(callbackid : str, chat_id : str):
    sql = "SELECT subject_id, department, speciality, course, groups FROM tasks WHERE id = %s"
    cursor.execute(sql, callbackid)

def register_handlers_tasks(dp : Dispatcher):
    dp.register_message_handler(cm_start, lambda message: message.text == "Переглянути завдання", state=UserRoles.teacher)
    dp.register_message_handler(mistake_departments, lambda message: message.text not in departments, state=FSMViewTasks.department)
    dp.register_message_handler(choose_department, state=FSMViewTasks.department)
    dp.register_message_handler(mistake_specialties, lambda message: message.text not in specialties, state=FSMViewTasks.speciality)
    dp.register_message_handler(choose_speciality, state=FSMViewTasks.speciality)
    dp.register_message_handler(mistake_course, lambda message: message.text not in ["1", "2", "3", "4", "5", "6"], state=FSMViewTasks.course)
    dp.register_message_handler(choose_course, state=FSMViewTasks.course)
    dp.register_message_handler(mistake_group, lambda message: message.text not in groups, state=FSMViewTasks.group)
    dp.register_message_handler(choose_group, state=FSMViewTasks.group)
    dp.register_callback_query_handler(callback_command, Text(endswith=['check','editTask', 'deleteTask']), state=UserRoles.teacher)