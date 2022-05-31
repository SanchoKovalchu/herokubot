from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from bot_create import cursor
from bot_create import bot
from handlers.login import UserRoles
class FormAnnounce(StatesGroup):
    receivers = State()
    course = State()
    sp = State()
    group = State()
    person = State()
    content = State()
    confirmation = State()


async def announcement_command(message: types.Message):
    # Set state
    await FormAnnounce.receivers.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Курс", "Спеціальність", "Група", "Студент", "Викладач")
    await message.reply("Хто має отримати повідомлення?", reply_markup=markup)

async def mistake_receivers(message: types.Message):
    return await message.reply("Помилка. Оберіть отримувачів з клавіатури")

async def load_receivers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['receivers'] = message.text
        user_receivers = data['receivers']
    if user_receivers == 'Викладач':
        await FormAnnounce.person.set()
        await message.reply("Введіть ПІБ викладача:")
    elif user_receivers != 'Студент':
        await FormAnnounce.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("1", "2", "3", "4", "5", "6")
        await message.reply("Який курс?", reply_markup=markup)
    else:
        await FormAnnounce.person.set()
        await message.reply("Введіть ПІБ студента:")

async def mistake_course(message: types.Message):
    return await message.reply("Помилка. Оберіть курс із клавіатури")

async def load_course(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = message.text
        user_receivers = data['receivers']
    if  user_receivers != 'Курс':
        await FormAnnounce.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("IPZ", "PP", "AND", "KN")
        await message.reply("Яка спеціальність?", reply_markup=markup)
    else:
        await FormAnnounce.content.set()
        await message.reply("Введіть текст повідомлення", reply_markup=types.ReplyKeyboardRemove())

async def mistake_sp(message: types.Message):
    return await message.reply("Помилка. Оберіть спеціальність із клавіатури")

async def load_sp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sp'] = message.text
        user_receivers = data['receivers']
    if  user_receivers != 'Спеціальність':
        await FormAnnounce.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("1", "2", "3", "4", "5")
        await message.reply("Яка група?", reply_markup=markup)
    else:
        await FormAnnounce.content.set()
        await message.reply("Введіть текст повідомлення", reply_markup=types.ReplyKeyboardRemove())

async def mistake_group(message: types.Message):
    return await message.reply("Помилка. Оберіть групу із клавіатури")

async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await FormAnnounce.content.set()
    await message.reply("Введіть текст повідомлення", reply_markup=types.ReplyKeyboardRemove())

async def load_PIB(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['PIB'] = message.text
    await FormAnnounce.content.set()
    await message.reply("Введіть текст повідомлення", reply_markup=types.ReplyKeyboardRemove())

async def load_content(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['content'] = message.text
        user_receivers = data['receivers']
        if user_receivers == 'Курс' or user_receivers == 'Спеціальність' or user_receivers == 'Група':
            user_course = data['course']
        if user_receivers == 'Спеціальність' or user_receivers == 'Група':
            user_sp = data['sp']
        if user_receivers == 'Група':
            user_group = data['group']
        if user_receivers == 'Студент' or user_receivers == 'Викладач':
            user_PIB = data['PIB']
        user_content = data['content']
    if user_receivers == 'Курс':
        await message.answer("Таке повідомлення буде надіслано студентам "+user_course+"-ого курсу:")
    elif user_receivers == 'Спеціальність':
        await message.answer("Таке повідомлення буде надіслано студентам "+user_course+"-ого курсу спеціальності "+user_sp+":")
    elif user_receivers == 'Група':
        await message.answer("Таке повідомлення буде надіслано студентам групи" + user_sp + "-" + user_course+user_group+":")
    elif user_receivers == 'Студент':
        await message.answer("Таке повідомлення буде надіслано студенту, ПІБ якого " + user_PIB+":")
    elif user_receivers == 'Викладач':
        await message.answer("Таке повідомлення буде надіслано викладачу, ПІБ якого " + user_PIB + ":")
    await message.answer(user_content)
    await FormAnnounce.confirmation.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Надіслати", "Відмінити")
    await message.reply("Надіслати повідомлення?", reply_markup=markup)

async def mistake_confirmation(message: types.Message):
    return await message.reply("Помилка. Оберіть відповідь із клавіатури")

async def load_confirmation(message: types.Message, state: FSMContext):
    if message.text == "Відмінити" :
        await message.answer("Відмінено відправку оголошення", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return
    else:
        async with state.proxy() as data:
            user_receivers = data['receivers']
            if user_receivers == 'Курс' or user_receivers == 'Спеціальність' or user_receivers == 'Група':
                user_course = data['course']
            if user_receivers == 'Спеціальність' or user_receivers == 'Група':
                user_sp = data['sp']
            if user_receivers == 'Група':
                user_group = data['group']
            if user_receivers == 'Студент' or user_receivers == 'Викладач':
                user_PIB = data['PIB']
            user_content = data['content']
        await state.finish()
        if user_receivers=='Курс':
            sql = "SELECT * FROM student_data WHERE course = %s"
            cursor.execute(sql, user_course)
            rec = cursor.fetchall()
        elif user_receivers=='Спеціальність':
            sql = "SELECT * FROM student_data WHERE course = %s AND sp = %s"
            cursor.execute(sql, (user_course, user_sp))
            rec = cursor.fetchall()
        elif user_receivers=='Група':
            sql = "SELECT * FROM student_data WHERE course = %s AND sp = %s AND st_group = %s"
            cursor.execute(sql, (user_course, user_sp, user_group))
            rec = cursor.fetchall()
        elif user_receivers=='Студент':
            sql = "SELECT * FROM student_data WHERE PIB = %s"
            cursor.execute(sql, user_PIB)
            rec = cursor.fetchall()
        else:
            sql = "SELECT * FROM teacher_data WHERE PIB = %s"
            cursor.execute(sql, user_PIB)
            rec = cursor.fetchall()
        for row in rec:
            await bot.send_message(row['user_id'], user_content)
        await message.answer("Оголошення надіслано успішно!", reply_markup=types.ReplyKeyboardRemove())

def register_handlers_announcement(dp: Dispatcher):
    dp.register_message_handler(announcement_command, lambda message: message.text == "Звичайне оголошення", state=UserRoles.teacher)
    dp.register_message_handler(mistake_receivers, lambda message: message.text not in ["Курс", "Спеціальність", "Група", "Студент", "Викладач"], state=FormAnnounce.receivers)
    dp.register_message_handler(load_receivers, state=FormAnnounce.receivers)
    dp.register_message_handler(mistake_course,lambda message: message.text not in ["1", "2", "3", "4", "5", "6"],state=FormAnnounce.course)
    dp.register_message_handler(load_course, state=FormAnnounce.course)
    dp.register_message_handler(mistake_sp, lambda message: message.text not in ["IPZ", "PP", "AND", "KN"],state=FormAnnounce.sp)
    dp.register_message_handler(load_sp, state=FormAnnounce.sp)
    dp.register_message_handler(mistake_group, lambda message: message.text not in ["1", "2", "3", "4", "5"],state=FormAnnounce.group)
    dp.register_message_handler(load_group, state=FormAnnounce.group)
    dp.register_message_handler(load_PIB, state=FormAnnounce.person)
    dp.register_message_handler(load_content, state=FormAnnounce.content)
    dp.register_message_handler(mistake_confirmation, lambda message: message.text not in ["Надіслати", "Відмінити"], state=FormAnnounce.confirmation)
    dp.register_message_handler(load_confirmation, state=FormAnnounce.confirmation)