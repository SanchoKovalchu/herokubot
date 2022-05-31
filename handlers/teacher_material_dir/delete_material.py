from aiogram import types, Dispatcher
from bot_create import cursor, bot, connection
from keyboard.teacher_keyboard import tch_keyboard
from aiogram.dispatcher.filters import Text
import asyncio

from handlers.login import UserRoles

buttons = [types.InlineKeyboardButton(text='Так', callback_data="True"),types.InlineKeyboardButton(text='Ні', callback_data="False")]
bool = types.InlineKeyboardMarkup().add(*buttons)

id = ''

async def cm_start_delete(callbackid : str, chat_id : str ):
    global id
    id = callbackid
    msg = await bot.send_message(chat_id,"Ви впевнені, що хочете видалити цей матеріал?", reply_markup=bool)
    await asyncio.create_task(delete_message(msg, 20))

async def callback_delete(call : types.CallbackQuery):
    global id
    if call.data == "True":
        delete_statement = "DELETE FROM file_storage where id = %s"
        cursor.execute(delete_statement, id)
        await call.answer("Видалення пройшло успішно!")
        await call.message.edit_text("Видалено!")
        connection.commit()
    else:
        await call.message.edit_text("Файл не було видалено.")
    await bot.send_message(call.from_user.id, "Повернення до меню...", reply_markup=tch_keyboard)


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await message.delete()

def register_handlers_files(dp : Dispatcher):
    dp.register_callback_query_handler(callback_delete, Text(equals=["True", "False"]), state=UserRoles.teacher)