from create_bot import dp, bot
from search import user_pull

from aiogram import Dispatcher

from unik_info import admins
#@dp.errors_handler()
async def errors_handler(update, exception):
    message = update.message
    message_text = message.text
    person = message.from_user.id
    username = message.from_user.username
    try:
        person = user_pull(person)[3]
    except:
        pass
    msg = 'Пользователь {} - {}\nполучил ошибку {}, когда написал "{}"'.format(person, username,exception.__repr__(), message_text)
    for admin in admins.keys():
        await bot.send_message(admins[admin], msg)

def register_handler_errors(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)