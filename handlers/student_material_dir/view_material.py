from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_create import cursor, bot
from aiogram import types, Dispatcher
from keyboard.discipline_keyboard import dsp_keyboard, disciplines
from keyboard.student_keyboard import st_keyboard
from handlers.student_material_dir.edit_material import cm_start_edit
from handlers.student_material_dir.delete_material import cm_start_delete
from aiogram.dispatcher.filters import Text

from handlers.login import UserRoles

class FSMViewFilesStudent(StatesGroup):
    discipline = State()
    choose_file = State()

async def cm_start(message: types.Message):
    await FSMViewFilesStudent.discipline.set()
    await bot.send_message(message.chat.id, "Виберіть дисципліну, файли якої хочете побачити", reply_markup=dsp_keyboard)

async def mistake_discipline(message: types.Message):
    return await message.reply("Помилка. Оберіть дисципліну з клавіатури")

def get_keyboard(data: str):
    callback_data_edit = str(data) + '_edit'
    callback_data_delete = str(data) + '_delete'
    buttons = [types.InlineKeyboardButton(text="Редагувати", callback_data=callback_data_edit),
                   types.InlineKeyboardButton(text="Видалити", callback_data=callback_data_delete)]
    keyboard = types.InlineKeyboardMarkup().add(*buttons)
    return keyboard

async def sql_read_file(message: types.message, state: FSMContext):
    await message.reply(f'Усі файли з дисципліни "{message.text}": ', reply_markup=st_keyboard)
    sql = "SELECT * FROM file_storage_student WHERE subject = %s"
    cursor.execute(sql, message.text)
    for row in cursor.fetchall():
        message_text = f'Назва: {row["file_name"]}\nОпис: {row["description"]}'
        match row["file_type"]:
            case 'photo':
                await bot.send_photo(message.chat.id, row["file_id"], caption=message_text, reply_markup=get_keyboard(row["id"]))
            case 'video':
                await bot.send_video(message.chat.id, row["file_id"], caption=message_text, reply_markup=get_keyboard(row["id"]))
            case 'audio':
                await bot.send_audio(message.chat.id, row["file_id"], caption=message_text, reply_markup=get_keyboard(row["id"]))
            case 'voice':
                await bot.send_voice(message.chat.id, row["file_id"], caption=message_text, reply_markup=get_keyboard(row["id"]))
            case 'animation':
                await bot.send_animation(message.chat.id, row["file_id"], caption=message_text, reply_markup=get_keyboard(row["id"]))
            case 'video_note':
                await bot.send_video_note(message.chat.id, row["file_id"], caption=message_text, reply_markup=get_keyboard(row["id"]))
            case _:
                await bot.send_document(message.chat.id, row["file_id"], caption=message_text, reply_markup=get_keyboard(row["id"]))
    await state.finish()
    await UserRoles.student.set()

async def callbacks_command(call: types.CallbackQuery):
    command = call.data.split(sep="_")[1]
    print("Hello")
    if command == "edit":
        await cm_start_edit(call.data, call.from_user.id)
    else:
        await cm_start_delete(call.data,call.from_user.id)

def register_handlers_files(dp : Dispatcher):
    dp.register_message_handler(cm_start, lambda message: message.text == "Переглянути матеріал", state=UserRoles.student)
    dp.register_message_handler(mistake_discipline, lambda message: message.text not in disciplines, state=FSMViewFilesStudent.discipline)
    dp.register_message_handler(sql_read_file, state=FSMViewFilesStudent.discipline)
    dp.register_callback_query_handler(callbacks_command, Text(endswith=['edit','delete']), state=UserRoles.student)