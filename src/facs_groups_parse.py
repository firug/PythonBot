import requests
from bs4 import BeautifulSoup, Tag, NavigableString
import json
import re

def get_facs():
    r = requests.get("https://dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable&ysclid=lo9gylwpkq445923938")
    soup = BeautifulSoup(r.text, "lxml")
    selector = soup.find("select", id="facultet")
    value_pat = r'value="(\d*)"'
    facs = {}
    for tag in selector:
        k = re.findall(value_pat, str(tag))
        if (len(k)):
            facs[tag.get_text()] = k[0]
    return facs

def get_groups():
    facs = get_facs()
    groups = {}
    for fac_name in facs.keys():
        data = {
            'FacID': facs[fac_name],
        }
        r= requests.post("https://dvgups.ru/index.php?Itemid=1246&option=com_timetable&view=newtimetable&ysclid=lo9gylwpkq445923938", data=data)
        soup = BeautifulSoup(r.text, "lxml")
        selector = soup.find_all("option")
        value_pat = r'value="(\d*)"'
        group_name = r'гр. (.+) - ([а-яА-Я ]+)'
        for elem in selector:
            k = re.findall(value_pat, str(elem))
            if len(k):
                try:
                    m = re.search(group_name, elem.get_text())
                    groups[k[0]] = [m.group(1), m.group(2).strip(), facs[fac_name], "None", fac_name, "None", "None"]
                except:
                    print(elem, m)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(groups, f, ensure_ascii=False, indent=4)

def load_data():
    with open('data.json') as f:
        d = json.load(f)
        for el in d:
            stroka = tuple([el] + d[el])
            import sqlite3
            db = sqlite3.connect('main_DB')
            cursor = db.cursor()
            cursor.execute("""INSERT INTO group_to_facs VALUES (?,?,?,?,?,?,?,?)""", stroka)
            db.commit()
            db.close()
    
if __name__ == "__main__":
    print(get_facs())
