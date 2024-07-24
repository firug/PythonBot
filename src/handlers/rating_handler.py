from create_bot import dp, bot
from aiogram import types, Dispatcher

import search
from rating_with_req import info_rating

#@dp.message_handler(commands=["Успеваемость"])
async def send_rating(message: types.Message):
	"""
	This handler will be called when user sends
	"успеваемость"
	"""
	try:
		data = search.user_pull(id=message.from_user.id)
	except:
		await message.answer("Данные неправильно сохранились")
		from .options_handler import get_info
		await get_info(message)
		return 
	group_line = search.names_parse(data[1])
	fullname = data[-1]
	try:
		new_msg = await message.answer("Ожидайте, идёт загрузка...")
		results = info_rating(username=fullname,
			group=group_line)
		await new_msg.delete()
		
		if results:
			msg = "Успеваемость указана в формате 'Твоя/План':\n\n"
			current_res = ""
			for result in results:
				tmp = result[2]
				if tmp == "-":
					tmp = 0
				current_res += "{}: {}/{}\n\n".format(result[0], tmp, result[1])
			if current_res:
				await message.answer(msg + current_res)
			else:
				raise FileNotFoundError
		else:
			await message.answer("Твоего имени нет с списке группы(")
	except FileNotFoundError:
		await message.answer("Для пользователя с таким именем успеваемость не найдена.\
			\nПроверь свои данные.")
		from .personalities_handler import change_info
		await change_info(message)
	else:
		from .options_handler import send_welcome
		await send_welcome(message)

def register_handlers_rating(dp: Dispatcher):
	dp.register_message_handler(send_rating, commands=["Успеваемость"])