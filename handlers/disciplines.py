from bot_create import cursor, bot
from aiogram import types, Dispatcher
from handlers.login import UserRoles
async def view_disciplines(message : types.Message):
    sql = "SELECT * FROM disciplines"
    cursor.execute(sql)
    for row in cursor.fetchall():
        await bot.send_message(message.chat.id, f'Назва дисципліни: {row["sb_full_name"]}\nАбревіатура: {row["sb_abr_name"]}\nКафедра: {row["cafedra_name"]}')

def register_handlers_disciplines(dp : Dispatcher):
    dp.register_message_handler(view_disciplines, lambda message: message.text == "Перелік дисциплін")