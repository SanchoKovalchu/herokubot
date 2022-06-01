from aiogram.contrib.fsm_storage.memory import MemoryStorage
import db_conn
from aiogram.dispatcher import Dispatcher
from aiogram import Bot
import os
storage = MemoryStorage()

#Ivan
# TOKEN_API = "5397374009:AAG5m7j5hSR1IyNAOhqe9vR0Ts27xapzIho"

##Nick
# TOKEN_API = "5118218655:AAEAYQzCRzpjppB-96ohx6PvPvCNpRHTm0c"

#MAIN
# TOKEN_API = "5302840148:AAGtGfjfQZWbwRn0mqPrv_rEqRhK9XEiarg"
TOKEN_API = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot, storage=storage)

connection = db_conn.getConnection()
cursor = connection.cursor()

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN_API}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)
# DB_URL = os.getenv('DATABASE_URL')

