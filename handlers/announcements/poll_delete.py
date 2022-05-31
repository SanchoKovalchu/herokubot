from aiogram import types, Dispatcher
from bot_create import cursor, bot, connection
from keyboard.teacher_keyboard import tch_keyboard
from aiogram.dispatcher.filters import Text
import asyncio
from handlers.login import UserRoles

buttons = [types.InlineKeyboardButton(text='Так', callback_data="True_"),types.InlineKeyboardButton(text='Ні', callback_data="False_")]
bool = types.InlineKeyboardMarkup().add(*buttons)
id = ''
message1 = ""
message2 = ""


async def cm_start_delete_poll(callbackid: str, chat_id: str, msg1: str, msg2: str):
    global message1, message2
    global id
    id = callbackid
    message1 = msg1
    message2 = msg2
    msg = await bot.send_message(chat_id, "Ви впевнені, що хочете видалити це опитування?", reply_markup=bool)
    await asyncio.create_task(delete_message(msg, 20))


async def callback_poll_delete(call: types.CallbackQuery):
    global id
    global message1, message2
    if call.data == "True_":
        delete_statement = "DELETE FROM poll_storage where id = %s"
        cursor.execute(delete_statement, id)
        await call.answer("Видалення пройшло успішно!")
        await call.message.edit_text("Видалено!")
        await asyncio.create_task(delete_message(message1, 0))
        await asyncio.create_task(delete_message(message2, 0))
        connection.commit()
    else:
        await call.message.edit_text("Файл не було видалено.")
    await bot.send_message(call.from_user.id, "Повернення до меню...", reply_markup=tch_keyboard)


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await message.delete()


def register_handlers_files(dp: Dispatcher):
    dp.register_callback_query_handler(callback_poll_delete, Text(equals=["True_", "False_"]), state=UserRoles.teacher)