from aiogram import executor
import asyncio

from create_bot import dp

async def on_shutdown(dispatcher):
	await dispatcher.storage.close()

from handlers import collecting_info_handler,\
	options_handler, personalities_handler, \
		rating_handler, settings_handler,\
			timetable_handler, update_handlers,\
				special_situations_handler,\
					errors_handlers

options_handler.register_handlers_options(dp)
collecting_info_handler.register_handlers_collecting_info(dp)
personalities_handler.register_handlers_personalities(dp)
rating_handler.register_handlers_rating(dp)
settings_handler.register_handlers_settings(dp)
timetable_handler.register_handlers_timetable(dp)
update_handlers.register_handlers_update(dp)

special_situations_handler.register_handlers_special(dp)

errors_handlers.register_handler_errors(dp)


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	executor.start_polling(dp, skip_updates=True)

