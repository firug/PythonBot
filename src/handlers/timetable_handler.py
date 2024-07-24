from create_bot import dp
from user_state import UserState

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from timetable import process, parse_date
from datetime import datetime, timedelta, date

import search
from unik_info import calls, weekdays

#@dp.message_handler(commands=["Расписание"])
async def send_shedule(message: types.Message):
	"""
	This handler will be called when user asks
	info about shedule by pushing button "/расписание" 
	"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	today_button = types.KeyboardButton(text="Сегодня")
	tommorow_button = types.KeyboardButton(text="Завтра")
	back_button = types.KeyboardButton(text='Назад')

	markup.row(today_button, tommorow_button)
	markup.add(back_button)
	row_line = "На какой день ты хочешь узнать расписание?\
	\nЕсли хочешь узнать расписание на конкретный день - введи дату в формате ДД.ММ.ГГ\
	\nРасписание также доступно по дням недели (здесь не получится смотреть даты прошедших дней)"
	await message.reply(row_line, reply_markup=markup)
	await UserState.date.set()

#@dp.message_handler(state=UserState.date)
async def send_timetable_for(message: types.Message, state: FSMContext):
	try:
		group_info_user = str(search.user_pull(message.from_user.id)[1])
	except IndexError:
		await message.answer("Данные неправильно сохранились")
		from .options_handler import get_info
		await get_info(message)
		return 
	row_line = message.text.strip().lower()
	if row_line == "назад":
		#выходим из state
		await state.finish()
		from .special_situations_handler import not_understand
		await not_understand(message)
	else:
		info = -1
		if row_line == "сегодня":
			await message.answer("Расписание на сегодня: \n")
			new_msg = await message.answer("Ожидайте, идёт загрузка...")
			info = process(group=group_info_user, agreement="С")
			await new_msg.delete()
		elif row_line == "завтра":
			await message.answer("Расписание на завтра: \n")
			new_msg = await message.answer("Ожидайте, идёт загрузка...")
			info = process(group=group_info_user, agreement="З")
			await new_msg.delete()
		else:
			# значит это кастомный день
			good_line = 0
			for key in weekdays.keys():
				if key in row_line:
					nessesary_day = weekdays[key]
					if datetime.now().weekday() <= nessesary_day:
						good_line = date.today() + timedelta(days=(nessesary_day-datetime.now().weekday()))
					else:
						good_line = date.today() + timedelta(days=(7 - datetime.now().weekday() + nessesary_day))
					if good_line:
						good_line = parse_date(good_line)
						await message.answer("Расписание на {}".format(good_line))
						new_msg = await message.answer("Ожидайте, идёт загрузка...")
						info = process(group=group_info_user, agreement=good_line)
						await new_msg.delete()
					break
			
			if not(good_line):
				try:
					under = row_line.split('.')
					if (int(under[2][-2:]) < 22):
						raise TimeoutError
					elif len(under[2]) == 2:
						under[2] = "20" + under[2]
					good_line = ".".join(under)
					under = list(map(int, under))
					our_date = datetime(under[2], under[1], under[0])
					if our_date < datetime(2022, 9, 1):
						raise TimeoutError
				except TimeoutError:
					await message.answer("Прошлое не в наших силах :(")
				except:
					await message.answer("Информация введена некорректно.\
						\nЕсли хочешь выйти из расписания, напиши 'назад'")
				else:
					await message.answer("Расписание на {}".format(good_line))
					new_msg = await message.answer("Ожидайте, идёт загрузка...")
					info = process(group=group_info_user, agreement=good_line)
					await new_msg.delete()
		if info == -1:
			pass
		elif len(info):
			msg = ""
			real_info = list(zip(info[0], info[1]))
			for i in range(len(real_info)):
				last = real_info[i][1]
				this_call = calls[real_info[i][0][0]]
				if last[2]:
					msg += real_info[i][0] + " " + " "+ ": " + "\n"+ last[0] + " " + "\n" + last[1] + "\n" + last[2] + "\n\n"
				else:
					msg += real_info[i][0] + " " + " " + ": " + "\n"+ last[0] + " " + "\n" + last[1] + "\n\n"
			if msg:
				await message.answer(msg)
		else:
			if row_line == "сегодня":
				await message.answer("Сегодня нет занятий :)")
			elif row_line == "завтра":
				await message.answer("Завтра нет занятий :)")
			elif row_line in weekdays.keys():
				if row_line == "пятница" or row_line == "суббота" or row_line=="среда":
					row_line = row_line[:-1] + "у"
				await message.answer("В {} нет занятий :)".format(row_line))
			else:
				await message.answer("{} нет занятий :)".format(row_line))

def register_handlers_timetable(dp: Dispatcher):
	dp.register_message_handler(send_shedule, commands=["Расписание"])
	dp.register_message_handler(send_timetable_for, state=UserState.date)
