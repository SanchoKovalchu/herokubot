from aiogram import types, Dispatcher
from bot_create import bot
from handlers.login import UserRoles
from keyboard import ab_keyboard


async def choose_command(message : types.Message):
    await bot.send_message(message.chat.id, "Виберіть вид оголошення", reply_markup=ab_keyboard)


def register_handlers_choose_announcement(dp : Dispatcher):
    dp.register_message_handler(choose_command, lambda message: message.text == "Оголошення", state=UserRoles.teacher)