from gettext import dpgettext
from create_bot import bot

from aiogram import types, Dispatcher
from unik_info import admins

from aiogram.types import InputFile

import search

import os

from timetable import for_update
import asyncio
from rating_with_req import rating
from unik_info import gr_ids

async def local_update():
    for gr_id in gr_ids:
        os.system("rm *.json")
        groupname = search.names_parse(gr_id)
        for_update(str(gr_id))
        await asyncio.sleep(1)
        rating(group=groupname, username="")
        await asyncio.sleep(1)
#@dp.message_handler(commands=['delete_files'])
async def delete_files(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in admins.values():
        os.system("rm *.json")
        who_is = None
        for key in admins.keys():
            if admins[key] == user_id:
                who_is = key
                break
        for key in admins.keys():
            msg = who_is + " " + "удалил все старые файлы"
            await bot.send_message(admins[key], msg)
    else:
        username = "Неизвестный"
        try:
            username = search.user_pull(user_id)
        except:
            pass
        for key in admins.keys():
            msg = username[3] + " " + "пытается пользоваться root правами"
            await bot.send_message(int(admins[key]), msg)

#dp.message_handler(commands=["update_files"])
async def update_files(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in admins.values():
        who_is = None
        for key in admins.keys():
            if admins[key] == user_id:
                who_is = key
                break
        for key in admins.keys():
            msg = who_is + " " + "начал обновление"
            await bot.send_message(admins[key], msg)
        event_loop = asyncio.get_event_loop()
        event_loop.create_task(local_update())
    else:
        username = "Неизвестный"
        try:
            username = search.user_pull(user_id)
        except:
            pass
        for key in admins.keys():
            msg = username[3] + " " + "пытается пользоваться root правами"
            await bot.send_message(int(admins[key]), msg)

#dp.message_handler(commands="статистика")
async def statistics(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in admins.values():
        path_of_db = "main_DB"
        await message.answer_document(InputFile(path_of_db))
    else:
        username = "Неизвестный"
        try:
            username = search.user_pull(user_id)
        except:
            pass
        for key in admins.keys():
            msg = username[3] + " " + "пытается пользоваться root правами"
            await bot.send_message(int(admins[key]), msg)

async def feedBack(message : types.Message):
    if str(message.from_user.id) not in admins.values():
        return
    try:
        msg = message.text.split()[1:]
        msg = " ".join(msg)
    except:
        return
    users_to_notify = search.get_users()
    print(len(users_to_notify))
    for user_id_el in users_to_notify:
        try:
            await bot.send_message(int(user_id_el[0]), msg)
        except:
            pass

def register_handlers_update(dp: Dispatcher):
    dp.register_message_handler(delete_files, commands=["delete_files"])
    dp.register_message_handler(update_files, commands=["update_files", "stop"])
    dp.register_message_handler(statistics, commands=['статистика'])
    dp.register_message_handler(feedBack, commands=["notify_users"])
