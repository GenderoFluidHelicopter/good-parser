import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
headers = {
    'user-agent': user
}


def get_html(url):
    r = requests.get(url, headers=headers)
    return r


def get_content(html):
    catalog = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product__info')
    for i in items:
        price = i.find('div', class_='product__price-main').get_text()
        price = price.replace(' ', '').replace('руб', '')
        name = i.find('a', class_='product__link').get_text()
        print(name)
        if name is None:
            continue
        catalog.append({
            'name': name,
            'price': price,
        })
    return catalog


def append_file(items, path):
    with open(path, 'a+', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for item in items:
            writer.writerow([item['name'], item['price']])


def parse():
    filename = 'goods.csv'
    with open(filename, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Названия товара', 'Цена товара (в рублях)'])
    for URL in ['https://toy69.ru/dlya-nee/falloimitatory/?page='+str(i) for i in range(1, 5)]:
        html = get_html(URL)
        if html.status_code == 200:
            html = get_content(html.text)
        else:
            print('Error')
        append_file(html, filename)


parse()