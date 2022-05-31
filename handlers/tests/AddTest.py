from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from handlers.tests import AddQuestions, PointsForQuestions
from handlers.login import UserRoles
from aiogram.dispatcher.filters.state import State, StatesGroup

class InputTest:
    subject = ""
    subject_list = ["Math", "OOP", "ASD"]
    subject_index = int(0)

class TestCreatinga(StatesGroup):
    creating = State()
    notcreating = State()

class TestCreatingt(StatesGroup):
    creating = State()
    notcreating = State()

class TestCreatingq(StatesGroup):
    creating = State()
    notcreating = State()

class TestCreatinge(StatesGroup):
    creating = State()
    notcreating = State()

async def add_test(message: types.Message):
    InputTest.subject = ""
    await message.answer("Оберіть назву предмета\n" + "\nПоточний предмет: " + InputTest.subject_list[0], reply_markup=await get_keyboard_subject())

async def get_keyboard_subject():
    await TestCreatinga.creating.set()
    buttons = []
    l = int(1)
    if InputTest.subject_index != 0:
        buttons.append(types.InlineKeyboardButton(text="<-", callback_data="a_Previous"))
        l = l + 1
    buttons.append(types.InlineKeyboardButton(text="Choose", callback_data="a_Choose"))
    if InputTest.subject_index != len(InputTest.subject_list) - 1:
        buttons.append(types.InlineKeyboardButton(text="->", callback_data="a_Next"))
        l = l + 1
    keyboard = types.InlineKeyboardMarkup(row_width=l)
    keyboard.add(*buttons)
    return keyboard

async def callbacks_subject(call: types.CallbackQuery):
    await TestCreatinga.notcreating.set()
    action = call.data.split("_")[1]
    if action == "Previous":
        InputTest.subject_index = InputTest.subject_index - 1
        await call.message.edit_text("Оберіть назву предмета\n" + "\nПоточний предмет: " + InputTest.subject_list[InputTest.subject_index], reply_markup=await get_keyboard_subject())
    elif action == "Next":
        InputTest.subject_index = InputTest.subject_index + 1
        await call.message.edit_text("Оберіть назву предмета\n" + "\nПоточний предмет: " + InputTest.subject_list[InputTest.subject_index], reply_markup=await get_keyboard_subject())
    else:
        InputTest.subject = InputTest.subject_list[InputTest.subject_index]
        await call.answer()
        AddQuestions.InputTest.question = []
        AddQuestions.InputTest.numofvars = []
        AddQuestions.InputTest.answervars = []
        AddQuestions.InputTest.user_tasknumber = -1
        AddQuestions.InputTest.Condition = 0
        AddQuestions.InputTest.numofquestions = 0
        AddQuestions.InputTest.tempvars = []
        AddQuestions.InputTest.toappend = ""
        AddQuestions.InputTest.answerstring = ""
        AddQuestions.InputTest.numofquestions = 0
        AddQuestions.InputTest.Points = int(1)
        await AddQuestions.AddQuestionsInp2.inputting.set()
        await call.message.answer("Оберіть дію\n", reply_markup=await AddQuestions.get_create_keyboard())

def register_handlers_addtest(dp: Dispatcher):
    dp.register_message_handler(add_test, lambda message: message.text == "Створити тест", state=UserRoles.teacher)
    dp.register_callback_query_handler(callbacks_subject, state=TestCreatinga.creating)
    dp.register_callback_query_handler(AddQuestions.callbacks_create, state=TestCreatingt.creating)
    dp.register_callback_query_handler(AddQuestions.callbacks_agree, state=TestCreatingq.creating)
    dp.register_callback_query_handler(PointsForQuestions.callbacks_value, state=TestCreatinge.creating)
    dp.register_message_handler(AddQuestions.input_question_text, state=AddQuestions.AddQuestionsInp2.inputting)