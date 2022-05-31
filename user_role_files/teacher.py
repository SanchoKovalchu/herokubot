from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import asyncio

from keyboard.material_keyboard import mtrl_keyboard
from keyboard.task_keyboard import task_keyboard
from keyboard.teacher_keyboard import tch_keyboard

from handlers.login import UserRoles

async def material_command(message: types.Message, state: FSMContext):
    # Set state
    await message.reply("Що зробити?", reply_markup=mtrl_keyboard)

async def task_command(message : types.Message, state : FSMContext):
    # Set state
    await message.reply("Що зробити?", reply_markup=task_keyboard)

async def cancel_handler(message: types.Message):
    await message.reply('Повертаюсь до меню...', reply_markup=tch_keyboard)

def register_handlers_teacher(dp: Dispatcher):
    dp.register_message_handler(material_command, lambda message: message.text == "Матеріал", state=UserRoles.teacher)
    dp.register_message_handler(task_command, lambda message : message.text == "Завдання", state=UserRoles.teacher)
    dp.register_message_handler(cancel_handler, lambda message: message.text == "Назад", state=UserRoles.teacher)