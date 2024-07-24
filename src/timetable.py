import requests
from bs4 import BeautifulSoup
import os.path
from datetime import datetime, timedelta, date
import search
import json

fix_hours = 7

def parse_date(date_of):
	this_day = str(date_of).split()[0].split("-")
	this_day = ".".join([this_day[-1], this_day[1], this_day[0]])
	return this_day

def split_name(name):
	word = ''
	for letter in name:
		if letter.lower() != letter:
			#если это заглавная буква
			word += " " + letter
		else:
			word += letter
	return word.strip()

def collect_timetable(group="52752", date_of="28.10.2022", path=''):

	first_streak = date(2022, 9, 1)
	row_data = list(map(int, date_of.split('.')))
	some_day = date(row_data[-1], row_data[1], row_data[0])
	while not(first_streak <= some_day < first_streak + timedelta(days=14)):
		# пока не в нужном диапазоне
		first_streak += timedelta(days=14)
	#пока что мы будем использовать свои выходные данные
	url = "https://www.dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable"
	# отправим post запрос
	filename = path + group + "_" + date_of + "_" +"schedule" + ".json"
	data = {
		"Time":parse_date(first_streak),
		'GroupID': group
	}

	r = requests.post(url=url, data=data, verify=False)
	
	soup = BeautifulSoup(r.text, "lxml")
	# под h3 с нашей датой находится наша таблица
	timetable = soup.find_all("h3")

	info = {}
	important_time = ""
	for time in timetable:
		if date_of in time.next_element:
			important_time = time
	if not(important_time):
		with open(filename, "w") as file:
			json.dump({}, file)
		return filename
	tb_for_today = important_time.next_sibling

	trs = tb_for_today.find_all("tr")

	counters = []
	info = []
	for tr in trs:
		tds = tr.find_all("td")
		subj_info = []
		for td_i in range(1, len(tds)):
			if td_i == (len(tds) - 1):
				subj_info.append(split_name(tds[td_i].text[:-1]))
			else:
				subj_info.append(tds[td_i].next_element.text)
		counter = tds[0].next_element.next_element.text.strip()
		counters.append(counter)
		info.append(subj_info[:2] + [subj_info[-1]])
	
	data = [counters, info]
	print(data)
	with open(filename, "w") as file:
		json.dump(data, file)
	return filename

def for_timetable(filename):
	with open(filename) as file:
		info = json.load(file)
	return info

def for_update(group, timeload):
	date_of = parse_date(timeload + timedelta(hours=fix_hours))
	collect_timetable(group=group, date_of=date_of, path='weekly/')


def process(group="52752", agreement="З"):
	if agreement == "С":
		date_of = parse_date(datetime.now() + timedelta(hours=fix_hours))
	elif agreement == "З":
		date_of = parse_date(datetime.now() + timedelta(days=1, hours=fix_hours))
	else:
		date_of = agreement
	filename = group + "_" + date_of + "_" +"schedule" + ".json"
	if os.path.exists(filename):
		return for_timetable(filename)
	else:
		filename = collect_timetable(group=group, date_of=date_of)
		return for_timetable(filename)

def main():
	print(process())

if __name__ == "__main__":
	main()