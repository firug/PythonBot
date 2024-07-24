from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
	group = State()
	username = State()
	date = State()