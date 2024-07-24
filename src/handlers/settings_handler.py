from create_bot import dp
from aiogram import types, Dispatcher

from user_state import UserState


#@dp.message_handler(commands=["настройки"])
async def send_settings(message: types.Message):
	"""
	This handler will be called when user sends
	"настройки" or "/настройки"
	"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	change_userinfo = types.KeyboardButton(text="Профиль")
	about_developers = types.KeyboardButton(text="О разработчиках")
	back_button = types.KeyboardButton(text="Назад")

	markup.row(change_userinfo, about_developers)
	markup.add(back_button)

	await message.answer("Что ты хочешь?", reply_markup=markup)

#@dp.message_handler(commands=["изменить_фио"])
async def change_username(message: types.Message):
	"""
	This handler will ...
	"""
	line = "Ой, похоже, я неверно записала твоё имя.\
	\n\nВведи своё фамилию, имя, отчество."

	await message.answer(line)
	await UserState.username.set()

#@dp.message_handler(commands=["изменить_группу"])
async def change_group(message: types.Message):
	"""
	This handler will ...
	"""
	line = "Ой, видимо, я что-то перепутала, давай исправим.\
	\n\nВведи номер своей группы."

	await message.answer(line)
	await UserState.group.set()

def register_handlers_settings(dp: Dispatcher):
	dp.register_message_handler(send_settings, commands=["настройки"])
	dp.register_message_handler(change_username, commands=["изменить_фио"])
	dp.register_message_handler(change_group, commands=["изменить_группу"])