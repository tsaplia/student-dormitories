import json
import re
import requests
from bs4 import BeautifulSoup as BS, NavigableString, Tag

BASE_URL = "https://www.stw.berlin"
MAIN_PAGE_URL = f"{BASE_URL}/wohnen/wohnheime"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

def get_hausing_list()->list[dict]:
    full_page = requests.get(MAIN_PAGE_URL, headers=headers)
    soup = BS(full_page.content, 'html.parser')
    elems = soup.select('article>a')
    lst = []
    for el in elems:
        lst.append({
            "url": f'{BASE_URL}/{el.attrs["href"]}',
            "title": el.select_one('h2').text
        })

    return lst

def get_adress_str(tag: Tag): 
    text_nodes = [child.strip() for child in tag.children if isinstance(child, NavigableString)]
    pattern = r"^(.*?[0-9]+[a-z]*)"
    first_line = re.search(pattern, text_nodes[0]).group()
    return f"{first_line} {text_nodes[-2]}"

def get_info(url: str):
    full_page = requests.get(url, headers=headers)
    soup = BS(full_page.content, 'html.parser')
    box = soup.select("article>div")[-1]
    adress = get_adress_str(box.select_one(".row .col-xs-10"))
    return {"adress": adress}

hausing_list = get_hausing_list()
for data in hausing_list:
    data.update(get_info(data["url"]))

with open('../data/data.json', 'w') as json_file:
    json.dump(hausing_list, json_file, indent=4)


