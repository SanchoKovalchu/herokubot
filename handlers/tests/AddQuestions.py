from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from handlers.tests import CorrectAnswer, PointsForQuestions, AddTest
from aiogram.dispatcher.filters.state import State, StatesGroup

class InputTest:
    question = []
    numofvars = []
    answervars = []
    user_tasknumber = -1
    Condition = 0
    Points = int(0)
    numofquestions = 0
    tempvars = []
    toappend = ""
    answerstring = ""

class AddQuestionsInp(StatesGroup):
    notinputting = State()
    inputting = State()

class AddQuestionsInp2(StatesGroup):
    notinputting = State()
    inputting = State()

class TestCreatingb(StatesGroup):
    creating = State()
    notcreating = State()

async def get_create_keyboard():
    await AddTest.TestCreatingt.creating.set()
    if InputTest.numofquestions == 0:
        buttons = [types.InlineKeyboardButton(text="Додати питання", callback_data="t_A2")]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard
    else:
        buttons = [types.InlineKeyboardButton(text="Додати варіант відповіді", callback_data="t_A1"),
                   types.InlineKeyboardButton(text="Додати питання", callback_data="t_A2"),
                   types.InlineKeyboardButton(text="Завершити створення тесту", callback_data="t_A3")]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard

async def get_keyboard_agree():
    await AddTest.TestCreatingq.creating.set()
    buttons = [types.InlineKeyboardButton(text="Змінити", callback_data="q_A1"),
               types.InlineKeyboardButton(text="Підтвердити", callback_data="q_A2")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

async def input_question_text(message: types.Message):
    await AddQuestionsInp.notinputting.set()
    InputTest.toappend = message.text
    await message.answer("Ви підтверджуєте введені дані?\n" + message.text, reply_markup=await get_keyboard_agree())

async def callbacks_create(call: types.CallbackQuery):
    await AddQuestionsInp.inputting.set()
    action = call.data.split("_")[1]
    if InputTest.Points == 1:
        if action == "A1":
            await call.message.edit_text("Введіть варіант відповіді")
            InputTest.Condition = 2
        elif action == "A2":
            if InputTest.user_tasknumber != -1:
                InputTest.answervars.append(InputTest.tempvars)
            InputTest.numofquestions = InputTest.numofquestions + 1
            InputTest.user_tasknumber = InputTest.user_tasknumber + 1
            InputTest.tempvars = []
            InputTest.numofvars.append(0)
            InputTest.Condition = 1
            await call.message.edit_text("Введіть текст питання")
        else:
            InputTest.answervars.append(InputTest.tempvars)
            CorrectAnswer.question=InputTest.question
            CorrectAnswer.answervars=InputTest.answervars
            CorrectAnswer.numofvars=InputTest.numofvars
            for i in range(0, len(InputTest.question)):
                InputTest.answerstring = InputTest.answerstring + "_"
            await AddTest.TestCreatingt.notcreating.set()
            await AddQuestionsInp.inputting.set()
            await CorrectAnswer.cmd_numbers(call.message)
    elif InputTest.Points == 2:
        if action == "A1":
            await call.message.edit_text("Введіть іншу кількість балів")
        else:
            PointsForQuestions.ThisClass.question_value.append(PointsForQuestions.ThisClass.toappend)
            await PointsForQuestions.update_num_value(call.message)

async def callbacks_agree(call: types.CallbackQuery):
    await AddTest.TestCreatingq.notcreating.set()
    action = call.data.split("_")[1]
    if InputTest.Points == 1:
        if action == "A1":
            await AddQuestionsInp.inputting.set()
            await call.message.edit_text("Введіть виправлені дані")
        else:
            if InputTest.Condition == 1:
                InputTest.question.append(InputTest.toappend)
            else:
                InputTest.tempvars.append(InputTest.toappend)
                InputTest.numofvars[len(InputTest.question) - 1] = InputTest.numofvars[len(InputTest.question) - 1] + 1
            await call.message.edit_text("Оберіть дію\n", reply_markup=await get_create_keyboard())
    elif InputTest.Points == 2:
        if action == "A1":
            await AddQuestionsInp2.inputting.set()
            await call.message.edit_text("Введіть іншу кількість балів")
        else:
            PointsForQuestions.ThisClass.question_value.append(InputTest.toappend)
            await PointsForQuestions.update_num_value(call.message)

def register_handlers_correct(dp: Dispatcher):
    dp.register_callback_query_handler(CorrectAnswer.callbacks_correct, state=TestCreatingb.creating)
    dp.register_message_handler(input_question_text, state=AddQuestionsInp.inputting)