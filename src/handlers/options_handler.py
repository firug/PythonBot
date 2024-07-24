from user_state import UserState
from create_bot import dp

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import search

from .personalities_handler import change_info

#@dp.message_handler(commands="start", state="*")
async def starter(message:types.Message, state: FSMContext):
    await state.finish()
    await get_info(message)

#@dp.message_handler(commands="get_info")
async def get_info(message: types.Message):
	try:
		search.user_pull(id=message.from_user.id)
	except IndexError:
		# если человек впервые
		text = """Привет, я бот ДВГУПС.\
		\nМеня зовут Лизи!\
		\nЯ создана для того, чтобы помочь тебе в суровой студенческой жизни.\
		\nНо для начала, давай познакомимся...
		\nКак тебя зовут? (ФИО)"""
		await message.answer(text)
		#setting user group
		await UserState.username.set()
	else:
		# если был до этого
		await change_info(message)


#@dp.message_handler(commands=["help", "назад"])
async def send_welcome(message: types.Message):
	"""
	This handler will be called when user sends 
	"/start" and "/help"
	"""
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	shedule_button = types.KeyboardButton(text="Расписание")
	rating_button = types.KeyboardButton(text="Успеваемость")

	settings_button = types.KeyboardButton(text="Настройки")
	keyboard.row(shedule_button, rating_button)
	keyboard.add(settings_button)
	msg_text = message.text.lower()
	if ("назад" in msg_text) or ("успеваемость" in msg_text) or \
	("измени" in msg_text) or ("всё верно"in msg_text) or ("о разработчиках" in msg_text):
		line = "Чем помочь?"
	else:
		line = "С чего начнём?"

	await message.answer(line, reply_markup=keyboard)

def register_handlers_options(dp: Dispatcher):
	dp.register_message_handler(starter, commands="start", state="*")
	dp.register_message_handler(get_info, commands="get_info")
	dp.register_message_handler(send_welcome, commands=["help", "назад"])