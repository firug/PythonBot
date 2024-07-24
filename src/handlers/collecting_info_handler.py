from create_bot import dp, bot
from user_state import UserState

from aiogram import types, Dispatcher
import re
import search
from aiogram.dispatcher import FSMContext

#@dp.message_handler(state=UserState.username)
async def get_username(message: types.Message, state: FSMContext):
	name = message.text.split()
	if len(name) != 3 or any(re.search('\d', one) for one in name):
		await message.answer("Вы ввели имя некорректно, попробуйте ещё раз.")
		await UserState.username.set()
	else:
		our_info = ' '.join([i.capitalize() for i in message.text.split()])
		try:
			# узнаём, пользовался ли пользователь ботом прежде
			search.user_pull(id=message.from_user.id)
		except IndexError:
			# значит user впервые, нужно продолжить сбор данных
			await state.update_data(username=our_info)
			text = "Приятно познакомиться, {}!\
			\nА теперь, позволь узнать мне... Из какой ты группы?".format(our_info.split()[1])
			await message.answer(text)
			await UserState.group.set()
		else:
			# если пользователь существует,
			# нужно будет изменить имя о нём
			search.user_name_ch(id=message.from_user.id,
                                newname=our_info)
			await state.finish()
			await message.answer("Имя изменено.")
			from .personalities_handler import change_info
			await change_info(message)


#@dp.message_handler(state=UserState.group)
async def get_usergroup(message: types.Message, state: FSMContext):
	try:
		# проверка на указание нормальной группы
		group_line = message.text.upper()
		info_group_inst = search.group_parse(group_line)
	except IndexError:
		info_line = "Прости, такую группу я не знаю.\
		\nПопробуй ещё раз ввести свою группу."
		await message.answer(info_line)
		await UserState.group.set()
	else:
		# если ввели нормальную группу
		try:
			# впервые ли пользователь определяется здесь
			search.user_pull(message.from_user.id)
		except IndexError:
			# если впервые
			await state.update_data(group=group_line)
			data_from_state = await state.get_data()
			try:
				search.user_add(id=message.from_user.id,
                            id_group=info_group_inst[0],
                            id_fac=info_group_inst[1],
                            fullname=data_from_state['username'])
			except:
				state.finish()
				from .options_handler import get_info
				await get_info(message)
				return 
			await state.finish()

			await message.answer("Вау, отлично!")
			line = "Сейчас я расскажу тебе немного о себе.\
			\n\nЯ могу выполнять несколько команд:\
			\n\nРасписание - позволит узнать расписание на сегодняшний и завтрашний день\
			\n\nУспеваемость - даст возможность увидеть свою успеваемость по всем предметам.\
			\n\nНастройки - тут ты сможешь изменить номер своей\
			группы или ФИО, в случае некорректного ввода.\
			Или прочитать о тех, кто меня создал:)"
			msg = await message.answer(line)
			await bot.pin_chat_message(message.from_user.id, msg.message_id)
			from .options_handler import send_welcome
			await send_welcome(message)
		else:
			# если хочет изменить группу
			search.user_group_ch(id=message.from_user.id,
                                 newgroup_id=info_group_inst[0])
			await state.finish()
			await message.answer("Номер группы изменён.")
			from .personalities_handler import change_info
			await change_info(message)

def register_handlers_collecting_info(dp: Dispatcher):
	dp.register_message_handler(get_username, state=UserState.username)
	dp.register_message_handler(get_usergroup, state=UserState.group)