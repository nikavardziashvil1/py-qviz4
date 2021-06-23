import requests
from bs4 import BeautifulSoup

URL_base = "https://www.myauto.ge/ka/s/00/0/2/00/00/00/00/audi?stype=0&marka=2&price_from=10000&price_to=20000&currency_id=3&det_search=0&ord=7&category_id=m0&keyword="

URL_pages = "https://www.myauto.ge/ka/s/00/0/2/00/00/00/00/audi?stype=0&marka=2&price_from=10000&price_to=20000&currency_id=3&det_search=0&ord=7&category_id=m0&keyword=&page="

h = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

r = requests.get(URL_base, headers=h)
c = r.content

soup = BeautifulSoup(c, "html.parser")

locator = "ul.pagination-ul li.last-page a"
data = soup.select_one(locator).attrs["href"]

number = data.find("page=") + 5

end = int(data[number:])

list_of_d = []

for page in range(1, end + 1):

    r = requests.get(URL_pages + str(page), headers=h)
    c = r.content

    soup = BeautifulSoup(c, "html.parser")

    data = soup.find("div", {"class": "search-lists-container"})
    data_rows = data.find_all("div", {"class": "current-item-inner"})

    for item in data_rows:
        d = {}

        d["განცხადება"] = item.find("h4", {"itemprop": "name"}).text.strip()
        d["ძრავი"] = item.find("div", {"data-info": "ძრავი"}).text.strip()

        d["გარბენი"] = item.find("div", {"data-engin": "გარბენი"}).text.strip()

        try:
            d["ლარი"] = item.find_all("span", {"class": "car-price"})[0].text.strip()
            d["დოლარი"] = item.find_all("span", {"class": "car-price"})[1].text.strip()
        except:
            d["ლარი"] = "ფასი შეთანხმებით"
            d["დოლარი"] = "ფასი შეთანხმებით"

        d["აღწერა"] = item.find("p", {"class": "car-list-paragraph"}).text.strip()

        list_of_d.append(d)

import pprint

# pprint.pprint(list_of_d)

print(len(list_of_d))