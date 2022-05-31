from aiogram import types, Dispatcher
from handlers.tests import AddQuestions, PointsForQuestions, AddTest

user_data = {}
question = []
answervars = []
numofvars = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class ThisClass:
    m = int(0)
    user_tasknumber = int(0)

async def get_keyboard(num: int):
    await AddQuestions.TestCreatingb.creating.set()
    if AddQuestions.InputTest.answerstring[num] == '_':
        buttons = []
        l = int(1)
        if num != 0:
            buttons.append(types.InlineKeyboardButton(text="Previous", callback_data="b_Previous"))
        for i in range(0, numofvars[ThisClass.user_tasknumber]):
            l = l + 1
            buttons.append(types.InlineKeyboardButton(text=alphabet[i], callback_data="b_" + alphabet[i]))
        if num != len(AddQuestions.InputTest.answerstring) - 1:
            l = l + 1
            buttons.append(types.InlineKeyboardButton(text="Next", callback_data="b_Next"))
        else:
            l = l + 1
            buttons.append(types.InlineKeyboardButton(text="End", callback_data="b_End"))
        keyboard = types.InlineKeyboardMarkup(row_width=l)
        keyboard.add(*buttons)
        return keyboard
    else:
        buttons = []
        l = int(1)
        if num != 0:
            l = l + 1
            buttons.append(types.InlineKeyboardButton(text="Previous", callback_data="b_Previous"))
        buttons.append(types.InlineKeyboardButton(text="Change answer", callback_data="b_Change"))
        if num != len(AddQuestions.InputTest.answerstring) - 1:
            l = l + 1
            buttons.append(types.InlineKeyboardButton(text="Next", callback_data="b_Next"))
        else:
            l = l + 1
            buttons.append(types.InlineKeyboardButton(text="End", callback_data="b_End"))
        keyboard = types.InlineKeyboardMarkup(row_width=l)
        keyboard.add(*buttons)
        return keyboard

async def cmd_numbers(message: types.Message):
    await AddTest.TestCreatingq.creating.set()
    user_data[message.from_user.id] = 0
    ThisClass.user_tasknumber = 0
    stringofans = ""
    for i in range(0, len(answervars[ThisClass.user_tasknumber])):
        stringofans = stringofans + answervars[ThisClass.user_tasknumber][i] + "\n"
    await message.answer("Питання " + str(ThisClass.user_tasknumber + 1) + "\n" + question[ThisClass.user_tasknumber] + "\nОберіть відповідь: \n" + stringofans, reply_markup=await get_keyboard(0))

async def update_num_text(message: types.Message):
    stringofans = ""
    for i in range(0, len(answervars[ThisClass.user_tasknumber])):
        stringofans = stringofans + answervars[ThisClass.user_tasknumber][i] + "\n"
    await message.edit_text("Питання " + str(ThisClass.user_tasknumber + 1) + "\n" + question[ThisClass.user_tasknumber] + "\nОберіть відповідь: \n" + stringofans, reply_markup=await get_keyboard(ThisClass.user_tasknumber))

async def callbacks_correct(call: types.CallbackQuery):
    await AddQuestions.TestCreatingb.notcreating.set()
    action = call.data.split("_")[1]
    if action == "Next":
        ThisClass.user_tasknumber = ThisClass.user_tasknumber + 1
        await update_num_text(call.message)
    elif action == "Previous":
        ThisClass.user_tasknumber = ThisClass.user_tasknumber - 1
        await update_num_text(call.message)
    elif action == "Change":
        AddQuestions.InputTest.answerstring = AddQuestions.InputTest.answerstring[:ThisClass.user_tasknumber] + "_" + AddQuestions.InputTest.answerstring[ThisClass.user_tasknumber + 1:]
        await update_num_text(call.message)
    elif action == "End":
        await AddTest.TestCreatingq.notcreating.set()
        await PointsForQuestions.cmd_value(call.message)
    else:
        AddQuestions.InputTest.answerstring = AddQuestions.InputTest.answerstring[:ThisClass.user_tasknumber] + str(action) + AddQuestions.InputTest.answerstring[ThisClass.user_tasknumber + 1:]
        await update_num_text(call.message)
    await call.answer()

def register_handlers_correctanswer(dp: Dispatcher):
    dp.register_message_handler(PointsForQuestions.input_question_value, state=AddQuestions.AddQuestionsInp2.inputting)