from aiogram import types
from handlers.tests import CorrectAnswer, AddQuestions, AddTest
from handlers.login import UserRoles

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class ThisClass:
    user_tasknumber = int(0)
    answerstring = ""
    m = int(0)
    user_tasknumber = int(0)
    toappend = ""
    question_value = []
    question = []
    answervars = []
    numofvars = []

async def get_keyboard_value():
    await AddTest.TestCreatinge.creating.set()
    buttons = [types.InlineKeyboardButton(text="Змінити", callback_data="e_A1"),
               types.InlineKeyboardButton(text="Підтвердити", callback_data="e_A2")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

async def cmd_value(message: types.Message):
    AddQuestions.InputTest.Points = 2
    ThisClass.user_tasknumber = 0
    ThisClass.question = CorrectAnswer.question
    ThisClass.answervars = CorrectAnswer.answervars
    ThisClass.numofvars = CorrectAnswer.numofvars
    ThisClass.answerstring = AddQuestions.InputTest.answerstring
    ThisClass.question_value = []
    stringofans = ""
    for i in range(0, len(ThisClass.answervars[ThisClass.user_tasknumber])):
        stringofans = stringofans + ThisClass.answervars[ThisClass.user_tasknumber][i] + "\n"
    await AddQuestions.AddQuestionsInp2.inputting.set()
    await message.answer("Питання " + str(ThisClass.user_tasknumber + 1) + "\n" + ThisClass.question[ThisClass.user_tasknumber] + "\n\n" + "Введіть кількість балів за це питання")

async def update_num_value(message: types.Message):
    if ThisClass.user_tasknumber == len(ThisClass.question) - 1:
        await AddQuestions.AddQuestionsInp2.notinputting.set()
        print(ThisClass.question)
        print(ThisClass.question_value)
        print(ThisClass.numofvars)
        print(ThisClass.answervars)
        print(ThisClass.answerstring)
        AddQuestions.InputTest.Points = 0
        await message.edit_text("Тест створено успішно!")
        await UserRoles.teacher.set()
    else:
        ThisClass.user_tasknumber = ThisClass.user_tasknumber + 1
        stringofans = ""
        for i in range(0, len(ThisClass.answervars[ThisClass.user_tasknumber])):
            stringofans = stringofans + ThisClass.answervars[ThisClass.user_tasknumber][i] + "\n"
        await AddQuestions.AddQuestionsInp2.inputting.set()
        await message.edit_text("Питання " + str(ThisClass.user_tasknumber + 1) + "\n" + ThisClass.question[ThisClass.user_tasknumber] + "\n\n" + "Введіть кількість балів за це питання")

async def input_question_value(message: types.Message):
    ThisClass.toappend = message.text
    await message.answer("Ви підтверджуєте введені дані?\n" + message.text, reply_markup=await get_keyboard_value())

async def callbacks_value(call: types.CallbackQuery):
    await AddTest.TestCreatinge.notcreating.set()
    action = call.data.split("_")[1]
    if action == "A1":
        await AddQuestions.AddQuestionsInp2.inputting.set()
        await call.message.edit_text("Введіть іншу кількість балів")
    else:
        ThisClass.question_value.append(ThisClass.toappend)
        AddQuestions.AddQuestionsInp2.notinputting.set()
        await update_num_value(call.message)