from aiogram import types, Dispatcher

import search

#@dp.message_handler(commands=['профиль'])
async def change_info(message: types.Message):
	"""
	This handler will ...
	"""
	try:
		user = search.user_pull(id=message.from_user.id)
	except IndexError:
		await message.answer("Данные неправильно сохранились")
		from .options_handler import get_info
		await get_info(message)
		return 
	group_line = search.names_parse(group_id=user[1])

	line = """Тебя зовут {0},\
	\nты из группы {1}.\
	\nИли я в чём-то ошиблась?"""\
	.format(user[-1], group_line)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	change_name = types.KeyboardButton(text="Изменить ФИО")
	change_group = types.KeyboardButton(text="Изменить группу")
	back_button = types.KeyboardButton(text="Всё верно")

	markup.row(change_name, change_group)
	markup.add(back_button)

	await message.answer(line, reply_markup=markup)

#@dp.message_handler(commands=["разработчики"])
async def about_devs(message: types.Message):
	"""
	This handler will send info about us
	"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	info_line = """\
	Ух ты! Ты решил узнать о тех, кто меня создал?\
	\nТогда слушай:
	\n\nФируз - https://vk.com/middledev
	\n\nДаня - https://vk.com/stulevtoday
	\n\nЛёва - https://vk.com/l_slonc
	\n\nПСПО ДВГУПС - https://vk.com/profkomkhv
	"""

	await message.answer(info_line, reply_markup=markup, disable_web_page_preview=True)
	from .options_handler import send_welcome
	await send_welcome(message)

def register_handlers_personalities(dp: Dispatcher):
	dp.register_message_handler(change_info, commands=["профиль"])
	dp.register_message_handler(about_devs, commands=["разработчики"])