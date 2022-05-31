import json
import aiogram.dispatcher.filters.state

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot_create import cursor, bot, connection
from handlers.login import UserRoles
from keyboard.student_keyboard import st_keyboard

# item to check
check = []


# state
class Form(aiogram.dispatcher.filters.state.StatesGroup):
    subject = aiogram.dispatcher.filters.state.State()


async def announcement_command(message: types.Message):
    global check
    await Form.subject.set()
    check.clear()

    query = "SELECT marks_information FROM students_marks WHERE id_student = %s" % message.chat.id
    cursor.execute(query)
    is_exists = cursor.fetchall()
    if not is_exists:
        await message.answer("<b>Unfortunately you don't have marks for now :(</b>", parse_mode='HTML',
                             reply_markup=types.ReplyKeyboardRemove())
        await UserRoles.student.set()

    else:
        subjects_list = []
        marks_list = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

        query = "SELECT marks_information FROM students_marks WHERE id_student = %s" % message.chat.id
        cursor.execute(query)

        for item in cursor.fetchall():
            marks_list = json.loads(item['marks_information'])

        for subject in marks_list:
            if subject["Subject"] not in subjects_list:
                subjects_list.append(subject["Subject"])
                markup.add(subject["Subject"])
                check.append(subject["Subject"])
        markup.add("Назад")
        check.append("Назад")

        await bot.send_message(message.chat.id, text='Оберіть предмет з якого ви бажаєте отримати оцінки: ',
                               reply_markup=markup)


async def mistake(message: types.Message):
    return await bot.send_message(message.chat.id, "В введіть значення з клавіатури.")


# load subject
async def load_subject(message: types.Message, state: FSMContext):
    marks_list = []
    messages = ""

    # setting data state
    async with state.proxy() as data:
        data['subject'] = message.text

    # checking if user doesn't return
    if data['subject'] != "Назад":
        query = "SELECT marks_information FROM students_marks WHERE id_student = %s" % message.chat.id
        cursor.execute(query)

        # getting the json item from db
        for item in cursor.fetchall():
            marks_list = json.loads(item['marks_information'])
        index = 1
        messages += f"<b>{data['subject']}</b>\n\n"

        # outputting information
        summary_mark = 0
        for item in marks_list:
            if item["Subject"] == data['subject']:
                messages += f'<b>{index}. {item["Comment"]}</b> \n      Оцінка за роботу : <b>{item["Mark"]}</b>\n      ' \
                            f'Вчитель, який виставив оцінку : <b>@{item["Teacher"]}</b>\n' \
                            f'      Дата виставлення : <b>{item["Date"]}</b>\n\n'
                summary_mark += float(item["Mark"])
                index = index + 1
        messages += f"<b>Сумарна оцінка за даний предмет : {summary_mark}</b>"
        await bot.send_message(message.chat.id, messages, parse_mode='HTML')

    # returning to menu
    await message.answer("<b>Повертаюсь до меню...</b>", parse_mode='HTML',
                         reply_markup=st_keyboard)
    await state.finish()
    await UserRoles.student.set()


def register_handlers_marks(dp: Dispatcher):
    dp.register_message_handler(announcement_command, lambda message: message.text == "Оцінки", state=UserRoles.student)
    dp.register_message_handler(mistake, lambda message: message.text not in check, state=Form.subject)
    dp.register_message_handler(load_subject, state=Form.subject)
