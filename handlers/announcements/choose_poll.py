from aiogram import types, Dispatcher
from bot_create import bot
from handlers.login import UserRoles
from keyboard import pb_keyboard


async def choose_command(message: types.Message):
    await bot.send_message(message.chat.id, "Що ви хочете зробити?", reply_markup=pb_keyboard)


def register_handlers_choose_poll(dp: Dispatcher):
    dp.register_message_handler(choose_command, lambda message: message.text == "Опитування", state=UserRoles.teacher)