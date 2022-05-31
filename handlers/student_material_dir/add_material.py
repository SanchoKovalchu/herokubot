from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import  State, StatesGroup
from keyboard.student_keyboard import st_keyboard
from keyboard.discipline_keyboard import dsp_keyboard, disciplines
from aiogram import types, Dispatcher
from bot_create import cursor, bot, connection

from handlers.login import UserRoles

class FSMFilesStudent(StatesGroup):
    discipline = State()
    document = State()
    name = State()
    description = State()

async def cm_start(message : types.Message):
    await FSMFilesStudent.discipline.set()
    await bot.send_message(message.chat.id, "Виберіть дисципліну, до якої хочете завантажити файл", reply_markup=dsp_keyboard)

async def mistake_disciplines(message: types.Message):
    return await message.reply("Помилка. Оберіть дисципліну з клавіатури")

async def choose_discipline(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
    await FSMFilesStudent.next()
    await bot.send_message(message.chat.id, "Відправте файл")


async def upload_file(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.content_type
        if data['type'] == 'photo':
            data['file_id'] = message.photo[0].file_id
        elif data['type'] == 'video':
            data['file_id'] = message.video.file_id
        elif data['type'] == 'voice':
            data['file_id'] = message.voice.file_id
        elif data['type'] == 'audio':
            data['file_id'] = message.audio.file_id
        elif data['type'] == 'animation':
            data['file_id'] = message.animation.file_id
        elif data['type'] == 'video_note':
            data['file_id'] = message.video_note.file_id
        else:
            data['file_id'] = message.document.file_id
    await FSMFilesStudent.next()
    await message.reply("Яка назва файлу?")


async def file_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMFilesStudent.next()
    await message.reply("Опишіть вміст файлу")


async def file_description(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    async with state.proxy() as data:
        sql = "INSERT INTO 	file_storage_student (file_name, description, file_id, file_type, subject) " \
              + " VALUES (%s, %s, %s, %s, %s) "
        # Выполнить sql и передать 3 параметра.
        subject = data['subject']
        file_type = data['type']
        file_id = data['file_id']
        name = data['name']
        description = data['description']
        cursor.execute(sql, (name, description, file_id, file_type, subject))
        connection.commit()
        await message.reply("ВСТАВЛЕНО!", reply_markup=st_keyboard)
        await state.finish()
        await UserRoles.student.set()

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok', reply_markup=st_keyboard)
    await UserRoles.student.set()

def register_handlers_files(dp : Dispatcher):
    dp.register_message_handler(cm_start, lambda message: message.text == "Додати матеріал", state=UserRoles.student)
    dp.register_message_handler(mistake_disciplines, lambda message: message.text not in disciplines, state=FSMFilesStudent.discipline)
    dp.register_message_handler(choose_discipline, state=FSMFilesStudent.discipline)
    dp.register_message_handler(upload_file,content_types = ['photo','video','audio','document','animation','video_note','voice'], state=FSMFilesStudent.document)
    dp.register_message_handler(file_name,  state=FSMFilesStudent.name)
    dp.register_message_handler(file_description, state=FSMFilesStudent.description)
    dp.register_message_handler(cancel_handler, state="*",commands='stop')
    dp.register_message_handler(cancel_handler, Text(equals='stop', ignore_case=True), state="*")