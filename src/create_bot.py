import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

dotenvPath = os.path.join(os.path.dirname(__file__), ".env")

if (os.path.exists(dotenvPath)):
    load_dotenv(dotenvPath)

TOKEN = os.getenv("TOKEN")
TEST_TOKEN = os.getenv("TEST_TOKEN")

#bot = Bot(token=TOKEN)
bot = Bot(token=TEST_TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
