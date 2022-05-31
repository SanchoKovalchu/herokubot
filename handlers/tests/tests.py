from aiogram import types, Dispatcher
from handlers.tests import test_json_decoder
from handlers.login import UserRoles
from aiogram.dispatcher.filters.state import State, StatesGroup

user_data = {}
user_answersave = {}
answerstring = ""
question = []
question_value = []
answervars = []
numofvars = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class ThisClass:
    m = int(0)
    user_tasknumber = int(0)
    buttons = []

class TestingInp(StatesGroup):
    testing = State()
    nottesting = State()

async def get_keyboard(num: int, line):
    ThisClass.buttons = []
    if test_json_decoder.MyClass.num2 == 0:
        l = int(1)
        if num != 0:
            ThisClass.buttons.append(types.InlineKeyboardButton(text="<-", callback_data="ans_Previous"))
            l = l + 1
        ThisClass.buttons.append(types.InlineKeyboardButton(text="Choose", callback_data="ans_Ch1"))
        if num != test_json_decoder.MyClass.num3:
            ThisClass.buttons.append(types.InlineKeyboardButton(text="->", callback_data="ans_Next"))
            l = l + 1
        keyboard = types.InlineKeyboardMarkup(row_width=l)
        keyboard.add(*ThisClass.buttons)
        return keyboard
    elif test_json_decoder.MyClass.num2 == 1:
        l = int(1)
        if test_json_decoder.MyClass.numoftests == 1:
            ThisClass.buttons.append(types.InlineKeyboardButton(text="Choose", callback_data="ans_Ch2"))
        else:
            if num != 0:
                l = l + 1
                types.InlineKeyboardButton(text="<-", callback_data="ans_Previous")
            ThisClass.buttons.append(types.InlineKeyboardButton(text="Choose", callback_data="ans_Ch2"))
            if num != test_json_decoder.MyClass.numoftests - 1:
                l = l + 1
                ThisClass.buttons.append(types.InlineKeyboardButton(text="->", callback_data="ans_Next"))
        keyboard = types.InlineKeyboardMarkup(row_width=l)
        keyboard.add(*ThisClass.buttons)
        return keyboard
    else:
        if str(line)[num] == '_':
            l = int(1)
            if num != 0:
                ThisClass.buttons.append(types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"))
            for i in range(0, numofvars[ThisClass.user_tasknumber]):
                l = l + 1
                ThisClass.buttons.append(types.InlineKeyboardButton(text=alphabet[i], callback_data="ans_"+alphabet[i]))
            if num != len(answerstring) - 1:
                l = l + 1
                ThisClass.buttons.append(types.InlineKeyboardButton(text="Next", callback_data="ans_Next"))
            else:
                l = l + 1
                ThisClass.buttons.append(types.InlineKeyboardButton(text="End", callback_data="ans_End"))
            keyboard = types.InlineKeyboardMarkup(row_width=l)
            keyboard.add(*ThisClass.buttons)
            return keyboard
        else:
            l = int(1)
            if num != 0:
                l = l + 1
                ThisClass.buttons.append(types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"))
            ThisClass.buttons.append(types.InlineKeyboardButton(text="Change answer", callback_data="ans_Change"))
            if num != len(answerstring) - 1:
                l = l + 1
                ThisClass.buttons.append(types.InlineKeyboardButton(text="Next", callback_data="ans_Next"))
            else:
                l = l + 1
                ThisClass.buttons.append(types.InlineKeyboardButton(text="End", callback_data="ans_End"))
            keyboard = types.InlineKeyboardMarkup(row_width=l)
            keyboard.add(*ThisClass.buttons)
            return keyboard

async def cmd_numbers(message: types.Message):
    await TestingInp.testing.set()
    user_data[message.from_user.id] = 0
    ThisClass.user_tasknumber = 0
    test_json_decoder.MyClass.num2 = 0
    test_json_decoder.MyClass.num3 = 0
    stringstr = ""
    user_answersave[message.from_user.id] = stringstr
    test_json_decoder.MyClass.num3 = len(test_json_decoder.subject_list) - 1
    await message.answer("Оберіть назву предмета\n" + "\nПоточний предмет: " + test_json_decoder.subject_list[0], reply_markup= await get_keyboard(0, stringstr))

async def update_num_text(message: types.Message, user_savedans):
    if test_json_decoder.MyClass.num2 == 0:
        await message.edit_text("Оберіть назву предмета\n" + "\nПоточний предмет: " + test_json_decoder.subject_list[ThisClass.user_tasknumber], reply_markup=await get_keyboard(ThisClass.user_tasknumber, user_savedans))
    elif test_json_decoder.MyClass.num2 == 1:
        await message.edit_text("Оберіть номер тесту\n" + "\nПоточний тест: " + str(ThisClass.user_tasknumber + 1), reply_markup=await get_keyboard(ThisClass.user_tasknumber, user_savedans))
    else:
        stringofans = ""
        for i in range(0, len(answervars[ThisClass.user_tasknumber])):
            stringofans = stringofans + answervars[ThisClass.user_tasknumber][i] + "\n"
        await message.edit_text("Питання " + str(ThisClass.user_tasknumber + 1) + "\n" + question[ThisClass.user_tasknumber] + "\nОберіть відповідь: \n" + stringofans, reply_markup=await get_keyboard(ThisClass.user_tasknumber, user_savedans))

async def callbacks_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    user_savedans = user_answersave.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    if action == "Ch1":
        test_json_decoder.MyClass.num2 = int(1)
        test_json_decoder.MyClass.subject = str(test_json_decoder.subject_list[ThisClass.user_tasknumber])
        ThisClass.user_tasknumber = 0
        await test_json_decoder.count_tests(test_json_decoder.MyClass.subject)
        if (test_json_decoder.MyClass.numoftests == 1):
            test_json_decoder.MyClass.num2 = int(1)
            await update_num_text(call.message, user_savedans)
        elif (test_json_decoder.MyClass.numoftests == 0):
            await call.message.edit_text("Немає тестів з цього предмета")
        else:
            test_json_decoder.MyClass.num3 = int(test_json_decoder.MyClass.numoftests) - 1
            await update_num_text(call.message, user_savedans)
    elif action == "Ch2":
        test_json_decoder.MyClass.num2 = int(2)
        test_json_decoder.MyClass.numoftest = ThisClass.user_tasknumber
        ThisClass.user_tasknumber = 0
        await test_json_decoder.get_info()
        stringstr = ""
        for i in range(0, len(answerstring)):
            stringstr = stringstr + "_"
        user_answersave[call.from_user.id] = stringstr
        await update_num_text(call.message, stringstr)
    elif action == "Next":
        ThisClass.user_tasknumber = ThisClass.user_tasknumber + 1
        await update_num_text(call.message, user_savedans)
    elif action == "Previous":
        ThisClass.user_tasknumber = ThisClass.user_tasknumber - 1
        await update_num_text(call.message, user_savedans)
    elif action == "Change":
        stringstr = user_savedans
        stringstr = stringstr[:ThisClass.user_tasknumber] + "_" + stringstr[ThisClass.user_tasknumber + 1:]
        user_answersave[call.from_user.id] = stringstr
        await update_num_text(call.message, stringstr)
    elif action == "End":
        for i in range(0, len(answerstring)):
            if user_savedans[i] == answerstring[i]:
                user_value = user_value + question_value[i]
        await TestingInp.nottesting.set()
        await call.message.edit_text(f"Сума балів: {user_value}")
        await UserRoles.student.set()
    else:
        stringstr = user_savedans
        stringstr = stringstr[:ThisClass.user_tasknumber] + str(action) + stringstr[ThisClass.user_tasknumber + 1:]
        user_answersave[call.from_user.id] = stringstr
        await update_num_text(call.message, stringstr)
    await call.answer()


def register_handlers_tests(dp: Dispatcher):
    dp.register_message_handler(cmd_numbers, lambda message: message.text == "Тестування", state=UserRoles.student)
    dp.register_callback_query_handler(callbacks_num, state=TestingInp.testing)