from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_create import cursor, bot, connection
from aiogram import types, Dispatcher
from keyboard.teacher_keyboard import tch_keyboard
from keyboard.task_keyboard import changes_keyboard

from handlers.login import UserRoles

class FSMEditTasks(StatesGroup):
    edit_file_info = State()
    change_name = State()
    change_description = State()
    change_file = State()

id = (str)
chat = (str)
msg = (str)

async def cm_start_edit(callbackid : str, chat_id : str, message : str):
    global id, chat, msg
    msg = message
    chat = chat_id
    id = callbackid
    await FSMEditTasks.edit_file_info.set()
    await bot.send_message(chat_id, "Які дані ви хочете змінити?", reply_markup=changes_keyboard)

async def mistake_variables(message:types.Message):
    return await message.reply("Помилка. Оберіть параметр з клавіатури.")

async def update_variables(message:types.Message, state: FSMContext):
    global id
    sql = 'SELECT * FROM tasks WHERE id = %s'
    cursor.execute(sql, id)
    async with state.proxy() as data:
        row = cursor.fetchone()
        data["name"] = row["task_name"]
        data["description"] = row["task_description"]
        data["file_id"] = row["file_id"]
        data['info'] = message.text
    if data['info'] == 'Все разом':
        await message.answer("Яка назва завдання?")
        await FSMEditTasks.change_name.set()
    elif data['info'] == 'Назва':
        await message.answer("Яка назва завдання?")
        await FSMEditTasks.change_name.set()
    elif data['info'] == 'Опис':
        await message.answer("Опишіть завдання")
        await FSMEditTasks.change_description.set()
    elif data['info'] == 'Файл':
        await message.answer("Відправте файл")
        await FSMEditTasks.change_file.set()

async def update_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    if data['info'] != 'Все разом':
        await update_database(state)
    else:
        await message.answer("Опишіть завдання")
        await FSMEditTasks.change_description.set()

async def update_description(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    if data['info'] != 'Все разом':
        await update_database(state)
    else:
        await message.answer("Відправте файл")
        await FSMEditTasks.change_file.set()

async def update_file(message : types.Message, state: FSMContext):
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
    await update_database(state)

async def update_database(state: FSMContext):
    global id
    global chat
    async with state.proxy() as data:
        update_statement = "UPDATE tasks set task_name = %s, task_description = %s, file_id = %s WHERE id = %s"
        cursor.execute(update_statement, (data['name'], data['description'], data['file_id'], id))
        connection.commit()
    await state.finish()
    await UserRoles.teacher.set()
    await bot.send_message(chat, "Зміни внесено до БД!", reply_markup=tch_keyboard)

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await UserRoles.teacher.set()
    await message.reply('Ok', reply_markup=tch_keyboard)

def register_handlers_tasks(dp : Dispatcher):
    dp.register_message_handler(mistake_variables, lambda message: message.text not in ["Все разом", "Назва", "Опис", "Файл"], state=FSMEditTasks.edit_file_info)
    dp.register_message_handler(update_variables, state=FSMEditTasks.edit_file_info)
    dp.register_message_handler(update_name, state=FSMEditTasks.change_name)
    dp.register_message_handler(update_description, state=FSMEditTasks.change_description)
    dp.register_message_handler(update_file, content_types = ['photo','video','audio','document','animation','video_note','voice'], state=FSMEditTasks.change_file)
    dp.register_message_handler(cancel_handler, state="*", commands='stop')
    dp.register_message_handler(cancel_handler, lambda message: message.text == 'stop', state="*")



