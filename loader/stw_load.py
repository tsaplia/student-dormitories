import json
import re
import requests
from bs4 import BeautifulSoup as BS, NavigableString, ResultSet, Tag

BASE_URL = "https://www.stw.berlin"
MAIN_PAGE_URL = f"{BASE_URL}/wohnen/wohnheime"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

def normalize_text(text):
    text = re.sub(r'[\u00a0\u2000-\u200b\u202f\u205f\u3000]', ' ', text)
    return text

def get_hausing_list() -> list[dict]:
    full_page = requests.get(MAIN_PAGE_URL, headers=headers)
    soup = BS(full_page.content, "html.parser")
    elems = soup.select("article>a")
    lst = []
    for el in elems:
        lst.append(
            {"url": f'{BASE_URL}/{el.attrs["href"]}', "title": el.select_one("h3").text}
        )

    return lst


def get_adress_str(tag: Tag):
    text_nodes = [
        child.strip() for child in tag.children if isinstance(child, NavigableString)
    ]
    pattern = r"^(.*?[0-9]+[a-z]*)"
    first_line = re.search(pattern, text_nodes[0]).group()
    return f"{first_line} {text_nodes[-2]}"


def get_apartments(set: ResultSet[Tag]):
    keys = ["number", "people", "space", "price", "waiting"]
    apartments = []
    for tag in set:
        values = map(lambda c: c.text, tag.select("td"))
        values = map(normalize_text, values)
        apartments.append(dict(zip(keys, values)))
    return apartments


def get_cords(tag: Tag):
    pattern = r"\[\s*([-+]?\d+\.\d+)\s*,\s*([-+]?\d+\.\d+)\s*\]"
    match = re.search(pattern, tag.text)
    return [match.group(2), match.group(1)]


def get_info(url: str):
    full_page = requests.get(url, headers=headers)
    soup = BS(full_page.content, "html.parser")
    box = soup.select("article>div")[-1]
    adress = get_adress_str(box.select_one(".row .col-xs-10"))
    apartments = get_apartments(soup.select(".apartment tbody tr:first-child"))
    [lat, lon] = get_cords(box.select_one("script"))
    return {"adress": adress, "apartments": apartments, "lat": lat, "lon": lon}


if __name__ == "__main__":
    hausing_list = get_hausing_list()
    print(f"Found {len(hausing_list)} hausings")

    for i, data in enumerate(hausing_list):
        print(f"{i+1}/{len(hausing_list)} {data['title']}")
        data.update(get_info(data["url"]))

    with open("../data/full_data.json", "w", encoding="utf-8") as json_file:
        json.dump(hausing_list, json_file, indent=2, ensure_ascii=False)

    print("Done")
