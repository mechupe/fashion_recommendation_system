import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

HEADERS = {
    'User-agent': '"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"'}

#
# def download_image(data):
#     r = requests.get(test_image, headers=HEADERS)
#     out = open(f"..\data\{i}.jpg", "wb")
#     out.write(r.content)
#     out.close()


# def parse_page(num_page):
men_clothes_url = f'https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3&page={2}'
women_clothes_url = f'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?page={1}'
response_man = requests.get(men_clothes_url, headers=HEADERS)
response_woman = requests.get(women_clothes_url, headers=HEADERS)

soap_man = bs(response_man.text, 'html.parser')
soap_woman = bs(response_woman.text, 'html.parser')

woman_cards = soap_man.find_all('div', class_='x-product-card__card')
man_cards = soap_man.find_all('div', class_='x-product-card__card')
list_links_man = []
list_links_woman = []
i = 0
for man_card in man_cards:
    man_url = 'https://www.lamoda.ru/' + man_card.find_next().get('href')
    response_man_card = requests.get(man_url, headers=HEADERS)
    soap_man_card = bs(response_man_card.text, 'html.parser')
    man_card_images = soap_man_card.find_all('img')
    for photo in man_card_images:
        i+=1
        url_image = 'http:' + photo.get('src')
        r = requests.get(url_image, headers=HEADERS)
        with open(f"..\data\{i}.jpg", "wb") as data_image:
            data_image.write(r.content)

