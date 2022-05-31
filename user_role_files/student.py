from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot_create import bot
import asyncio

from keyboard.student_keyboard import st_keyboard
from keyboard.material_keyboard import mtrl_keyboard
from handlers.login import UserRoles

async def material_command(message: types.Message, state: FSMContext):
    # Set state
    await message.reply("Що зробити?", reply_markup=mtrl_keyboard)

async def cancel_handler(message: types.Message):
    await message.reply('Повертаюсь до меню...', reply_markup=st_keyboard)

def register_handlers_teacher(dp: Dispatcher):
    dp.register_message_handler(material_command, lambda message: message.text == "Матеріал", state=UserRoles.student)
    dp.register_message_handler(cancel_handler, lambda message: message.text == "Назад", state=UserRoles.student)