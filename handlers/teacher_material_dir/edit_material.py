from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_create import cursor, bot, connection
from aiogram import types, Dispatcher
from keyboard.discipline_keyboard import dsp_keyboard, disciplines
from keyboard.teacher_keyboard import tch_keyboard
from keyboard.file_keyboard import fl_keyboard

from handlers.login import UserRoles

class FSMEditFiles(StatesGroup):
    edit_file_info = State()
    change_name = State()
    change_description = State()
    change_subject = State()

id = ''
chat = ''

async def cm_start_edit(callbackid : str, chat_id : str):
    global id, chat
    chat = chat_id
    id = callbackid
    await FSMEditFiles.edit_file_info.set()
    await bot.send_message(chat_id, "Які дані ви хочете змінити?", reply_markup=fl_keyboard)

async def mistake_variables(message:types.Message):
    return await message.reply("Помилка. Оберіть параметр з клавіатури.")

async def update_variables(message:types.Message, state: FSMContext):
    global id
    sql = 'SELECT * FROM file_storage WHERE id = %s'
    cursor.execute(sql, id)
    async with state.proxy() as data:
        row = cursor.fetchone()
        data["name"] = row["file_name"]
        data["description"] = row["description"]
        data["subject"] = row["subject"]
        data['info'] = message.text
    if data['info'] == 'Все разом':
        await message.answer("Яка назва файлу?")
        await FSMEditFiles.change_name.set()
    elif data['info'] == 'Назва':
        await message.answer("Яка назва файлу?")
        await FSMEditFiles.change_name.set()
    elif data['info'] == 'Опис':
        await message.answer("Опишіть вміст файлу")
        await FSMEditFiles.change_description.set()
    elif data['info'] == 'Предмет':
        await message.answer("Виберіть дисципліну", reply_markup=dsp_keyboard)
        await FSMEditFiles.change_subject.set()

async def update_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    if data['info'] != 'Все разом':
        await update_database(state)
    else:
        await message.answer("Опишіть вміст файлу")
        await FSMEditFiles.change_description.set()

async def update_description(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    if data['info'] != 'Все разом':
        await update_database(state)
    else:
        await message.answer("Виберіть дисципліну", reply_markup=dsp_keyboard)
        await FSMEditFiles.change_subject.set()

async def mistake_subject(message : types.Message):
    return await message.reply("Помилка. Оберіть дисципліну з клавіатури")

async def update_subject(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
    await update_database(state)

async def update_database(state: FSMContext):
    global id
    global chat
    async with state.proxy() as data:
        update_statement = "UPDATE file_storage set file_name = %s, description = %s, subject = %s WHERE id = %s"
        cursor.execute(update_statement, (data['name'], data['description'], data['subject'], id))
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

def register_handlers_files(dp : Dispatcher):
    dp.register_message_handler(mistake_variables, lambda message: message.text not in ["Все разом", "Назва", "Опис", "Предмет"], state=FSMEditFiles.edit_file_info)
    dp.register_message_handler(update_variables, state=FSMEditFiles.edit_file_info)
    dp.register_message_handler(update_name, state=FSMEditFiles.change_name)
    dp.register_message_handler(update_description, state=FSMEditFiles.change_description)
    dp.register_message_handler(mistake_subject, lambda message: message.text not in disciplines, state=FSMEditFiles.change_subject)
    dp.register_message_handler(update_subject, state=FSMEditFiles.change_subject)
    dp.register_message_handler(cancel_handler, state="*", commands='stop')
    dp.register_message_handler(cancel_handler, lambda message: message.text == 'stop', state="*")



