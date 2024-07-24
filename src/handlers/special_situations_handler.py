from create_bot import dp
from aiogram import types, Dispatcher

from user_state import UserState
from aiogram.dispatcher.filters import Command

from .timetable_handler import send_shedule, send_timetable_for
from .options_handler import send_welcome
from .rating_handler import send_rating
from .settings_handler import send_settings, change_username, change_group
from .personalities_handler import change_info, about_devs

#@dp.message_handler()
async def not_understand(message:types.Message):
	row = message.text.strip().lower()
	help_words = ['help', 'помоги', "помогите"]
	if "расписание" in row:
		await send_shedule(message)
	elif ("сегодня" in row) or ("завтра" in row):
		await send_timetable_for(message, UserState.date)
	elif "успеваемость" in row:
		await send_rating(message)
	elif "настройки" in row:
		await send_settings(message)
	elif "профиль" in row:
		await change_info(message)
	elif "изменить фио" in row:
		await change_username(message)
	elif "изменить группу" in row:
		await change_group(message)
	elif "всё верно" in row:
		await send_welcome(message)
	elif ("назад" in row) or (any([(word in row) for word in help_words])):
		await send_welcome(message)
	elif "о разработчиках" in row:
		await about_devs(message)
	#elif "delete_file" in row:
		#from .update_handlers import delete_files
		#await delete_files(message)
	else:
		await message.answer("Прости, не понимаю тебя")

def register_handlers_special(dp: Dispatcher):
	dp.register_message_handler(not_understand)