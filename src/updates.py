import search
import re
import asyncio
import os
from unik_info import calls, gr_ids

from datetime import datetime, timedelta

from timetable import for_update
from rating_with_req import rating

"""
async def daily_update():
	print(str(datetime.now()))
	last_flag = False
	fix_to_hours = 60 * 60
	hour = (datetime.now() + timedelta(hours=7)).hour
	print(hour)
	if (24 - hour) <= 16:
		# если вечер или день
		print("sleep for {} hours".format(28 - hour))
		await asyncio.sleep((28 - hour)*fix_to_hours)
		last_flag = True
	else:
		while True:
			os.system("rm *.json")
			for gr_id in gr_ids:
				print("I am here")
				groupname = search.names_parse(gr_id)
				for_update(str(gr_id))
				await asyncio.sleep(1)
				rating(group=groupname, username="")
				await asyncio.sleep(1)
			if not(last_flag):
				# если это первое обновление
				await asyncio.sleep((28 - hour)*fix_to_hours)
				last_flag = True
			else:
				await asyncio.sleep(24*fix_to_hours)
async def weekly_update():
	nowaday = (datetime.now()+timedelta(hours=fix_hours) + timedelta(days=2)).weekday()
	if (nowaday == 6):
		# если сейчас воскресенье, значит ждём 6 дней
		print(6)
		await asyncio.sleep(6 * 24 * 60 * 60)
	elif (nowaday != 5):
		print(days)
		days = 6- nowaday
		await asyncio.sleep(days * 24 * 60 * 60)
	if (nowaday == 5):
		now = datetime.now() + timedelta(hours=fix_hours)+ timedelta(days=2)
		while True:
			os.system("rm weekly/*.json")
			for gr_id in gr_ids:
				groupname = search.names_parse(gr_id)
				for i in range(2, 9):
					# дни расписаний
					print((now+timedelta(days=i)).weekday())
					for_update(groupname, now+timedelta(days=i))
				
			asyncio.sleep(timedelta(days=1))
"""