import requests
from bs4 import BeautifulSoup
import re
import json
from timetable import parse_date
from datetime import datetime, timedelta
import os.path

fix_hours = 7
def rating(group, username):
	if username:
		name = username.split()
	else:
		name = ["","",""]
	today = parse_date(datetime.now() + timedelta(hours=fix_hours))
	filename = str(group) + "_" + today + "_" + "rating" + ".json"
	if os.path.exists(filename):
		return filename
	else:
		with requests.Session() as s:

			headers = {
				'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
				'Accept': '*/*',
				'Accept-Language': 'en-US,en;q=0.5',
				# 'Accept-Encoding': 'gzip, deflate, br',
			}
			response = s.get('https://studentrating.dvgups.ru/FindStudent.aspx', verify=False, headers=headers)
			#response = s.request("get","https://studentrating.dvgups.ru/ChoiceGroupSt.aspx")

			dummy_soup = BeautifulSoup(response.content, "lxml")
			viewstate = dummy_soup.select("#__VIEWSTATE")[0]["value"]
			viewstategen = dummy_soup.select("#__VIEWSTATEGENERATOR")[0]["value"]
			eventvalidation = dummy_soup.select("#__EVENTVALIDATION")[0]["value"]
			#event_target = dummy_soup.select("#__EVENTTARGET")[0]["value"]
			data = {
				'ctl00$ScriptManager1': 'ctl00$UpdatePanel2|ctl00$ContentPlaceHolder1$Button1',
				'__EVENTTARGET': "",
				'__EVENTARGUMENT': '',
			    '__VIEWSTATE': viewstate,
			    '__VIEWSTATEGENERATOR': viewstategen,
			    '__EVENTVALIDATION': eventvalidation,
			    'ctl00$DropDownList1': '24',
			    'ctl00$DropDownList2': '1',
			    'ctl00$ContentPlaceHolder1$TextBoxGroup': group,
			    'ctl00$ContentPlaceHolder1$TextBoxLastName': "",
			    'ctl00$ContentPlaceHolder1$TextBoxFirstName': "",
			    'ctl00$ContentPlaceHolder1$TextBoxFatherName': "",
			    '__ASYNCPOST': 'true',
			    'ctl00$ContentPlaceHolder1$Button1': 'Принять',
			}
			response = s.post("https://studentrating.dvgups.ru/FindStudent.aspx",data=data, headers=headers)
			response = s.get('https://studentrating.dvgups.ru/ChoiceGroupSt.aspx', verify=False, headers=headers)
			

			dummy_soup = BeautifulSoup(response.content, "lxml")
			with open("some.html", "w") as file:
				file.write(dummy_soup.prettify())
			viewstate = dummy_soup.select("#__VIEWSTATE")[0]["value"]
			viewstategen = dummy_soup.select("#__VIEWSTATEGENERATOR")[0]["value"]
			eventvalidation = dummy_soup.select("#__EVENTVALIDATION")[0]["value"]
			#event_target = dummy_soup.select("#__EVENTTARGET")[0]["value"]

			data ={
				"ctl00$ScriptManager1": "ctl00$ContentPlaceHolder1$UpdatePanel3|ctl00$ContentPlaceHolder1$GridView1$ctl02$LinkButton1",
				"__EVENTTARGET": "ctl00$ContentPlaceHolder1$GridView1$ctl02$LinkButton1",
				"__EVENTARGUMENT": "",
				"__LASTFOCUS": "",
				"__VIEWSTATE": viewstate,
				"__VIEWSTATEGENERATOR": viewstategen,
				"__EVENTVALIDATION": eventvalidation,
				"ctl00$DropDownList1": "24",
				"ctl00$DropDownList2": "1",
				"__ASYNCPOST": "true",
				"": ""
			}

			response = s.post("https://studentrating.dvgups.ru/ChoiceGroupSt.aspx", data=data, headers=headers)
			response = s.get("https://studentrating.dvgups.ru/RatingAll.aspx", verify=False, headers=headers)

			soup = BeautifulSoup(response.text, "lxml")
			
			table = soup.find("table", id="ctl00_ContentPlaceHolder1_ASPxGridView1_DXMainTable")
			headers = soup.find("tr", id="ctl00_ContentPlaceHolder1_ASPxGridView1_DXHeadersRow")
			table = table.find_all("tr")
			data_trs = []
			for tr in table:
				pattern = "ctl00_ContentPlaceHolder1_ASPxGridView1_DXDataRow\d{1,2}"
				if tr.get("id") and re.match(pattern, tr.get("id")):
					data_trs.append(tr)

			headers_info = []
			data_info = {}
			for td in headers:
				if td.text.strip():
					headers_info.append(td.text.strip())

			for tr_i in range(len(data_trs)):
				person_info = []
				for td in data_trs[tr_i]:
					if td.text.strip():
						person_info.append(td.text.strip())
				data_info[person_info[0]] = person_info[1:]
			data_info["Заголовки"] = headers_info[1:]

			with open(filename, "w") as file:
				json.dump(data_info, file)
	return filename

def info_rating(group, username):
	filename = rating(group, username)
	with open(filename) as file:
		info = json.load(file)
	if username in info.keys():
		k = zip(info["Заголовки"], info["План"],info[username])
		return list(k)
	else:
		return ""

def main():
	info_rating("БО221ПИН", "Гафоров Фируз Мухаммадшарифович")

if __name__ == "__main__":
	main()
