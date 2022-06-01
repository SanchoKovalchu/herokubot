import logging
from aiogram import executor, types
from handlers import login

from handlers.announcements import announcement, choose_poll, poll_announcement, poll_view, poll_delete, \
    choose_announcement

from handlers import disciplines
from handlers.marks import marks
from handlers.marks import add_marks as t_marks
from handlers.marks import edit_marks
from handlers.marks import watch_marks

from handlers.register_dir import admin_register
from handlers.register_dir import teacher_register
from handlers.register_dir import student_register

from handlers.teacher_material_dir import add_material as t_add
from handlers.teacher_material_dir import add_additional_material as t_add_additional
from handlers.teacher_material_dir.announcement_add_material import send_message
from handlers.teacher_material_dir import edit_material as t_edit
from handlers.teacher_material_dir import delete_material as t_delete
from handlers.teacher_material_dir import view_material as t_view

from handlers.teacher_task_dir import view_task as t_view_task, add_task as t_add_task, delete_task as t_delete_task, edit_task as t_edit_task

from handlers.student_material_dir import add_material as s_add
from handlers.student_material_dir import edit_material as s_edit
from handlers.student_material_dir import delete_material as s_delete
from handlers.student_material_dir import view_material as s_view

from bot_create import bot, dp, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from keyboard import first_keyboard
from user_role_files import teacher, student

from handlers.tests import tests, CorrectAnswer, AddTest, AddQuestions

###
import aioschedule
import asyncio

from aiogram.utils.executor import start_webhook

###
# teacher material
t_add.register_handlers_files(dp)
t_add_additional.register_handlers_files(dp)
t_edit.register_handlers_files(dp)
t_delete.register_handlers_files(dp)
t_view.register_handlers_files(dp)
# teacher tasks
t_add_task.register_handlers_tasks(dp)
t_view_task.register_handlers_tasks(dp)
t_delete_task.register_handlers_tasks(dp)
t_edit_task.register_handlers_tasks(dp)
#student tasks

# student material
s_add.register_handlers_files(dp)
s_edit.register_handlers_files(dp)
s_delete.register_handlers_files(dp)
s_view.register_handlers_files(dp)
# login and register
login.register_handlers_login(dp)
student_register.register_handlers_student_register(dp)
teacher_register.register_handlers_teacher_register(dp)
admin_register.register_handlers_admin_register(dp)
teacher.register_handlers_teacher(dp)
student.register_handlers_teacher(dp)

announcement.register_handlers_announcement(dp)
poll_announcement.register_handlers_poll_announcement(dp)
choose_announcement.register_handlers_choose_announcement(dp)
choose_poll.register_handlers_choose_poll(dp)
poll_view.register_handlers_poll_view(dp)
poll_delete.register_handlers_files(dp)

disciplines.register_handlers_disciplines(dp)
marks.register_handlers_marks(dp)
t_marks.register_handlers_marks(dp)
edit_marks.register_handlers_marks(dp)
watch_marks.register_handlers_marks(dp)

tests.register_handlers_tests(dp)
CorrectAnswer.register_handlers_correctanswer(dp)
AddTest.register_handlers_addtest(dp)
AddQuestions.register_handlers_correct(dp)



logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Ласкаво прошу до StudyBot!", reply_markup=first_keyboard)



async def scheduler():
    aioschedule.every(60).seconds.do(send_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    asyncio.create_task(scheduler())


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
