import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path

HEADERS = {
    'User-agent': '"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"'}
data_dir = Path('..\..\data')
#
# def download_image(data):
#     r = requests.get(test_image, headers=HEADERS)
#     out = open(f"..\data\{i}.jpg", "wb")
#     out.write(r.content)
#     out.close()

men_clothes_url = f'https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3&page='
women_clothes_url = f'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?page='


def parse_page(num_page, link, gender):
    clothes_url = link + str(num_page)
    response = requests.get(clothes_url, headers=HEADERS, timeout=100)
    soap = bs(response.text, 'html.parser')
    cards = soap.find_all('div', class_='x-product-card__card')
    labels_soap = soap.find_all('div', class_='x-product-card-description__product-name')
    labels = [label.text.split(' ')[1] for label in labels_soap]

    card_label = 0
    picture_num = 0

    for card in cards:
        data_dir = Path(f'..\data\{gender}\{labels[card_label]}')
        try:
            data_dir.mkdir()
        except FileExistsError:
            pass
        url = 'https://www.lamoda.ru/' + card.find_next().get('href')
        response_card = requests.get(url, headers=HEADERS)
        soap_card = bs(response_card.text, 'html.parser')
        card_images = soap_card.find_all('img')

        for photo in card_images:
            url_image = 'http:' + photo.get('src')
            r = requests.get(url_image, headers=HEADERS)

            with open(f'{str(data_dir).rstrip()}\\{picture_num}.jpg', "wb") as data_image:
                data_image.write(r.content)
            picture_num += 1
        card_label += 1


for i in range(1, 6):
    parse_page(i, men_clothes_url, 'MEN')
    parse_page(i, women_clothes_url, 'WOMEN')
# response_man = requests.get(men_clothes_url, headers=HEADERS, timeout=100)
# response_woman = requests.get(women_clothes_url, headers=HEADERS, timeout=100)
#
# soap_man = bs(response_man.text, 'html.parser')
# soap_woman = bs(response_woman.text, 'html.parser')
#
# woman_cards = soap_woman.find_all('div', class_='x-product-card__card')
# man_cards = soap_man.find_all('div', class_='x-product-card__card')
# man_labels_soap = soap_man.find_all('div', class_='x-product-card-description__product-name')
# woman_labels_soap = soap_woman.find_all('div', class_='x-product-card-description__product-name')
# man_labels = [label.text.split(' ')[1] for label in man_labels_soap]
# woman_labels = [label.text.split(' ')[1] for label in woman_labels_soap]
#
# card_label = 0
# picture_num = 0
# for man_card in man_cards:
#     data_dir = Path(f'..\data\MEN\{man_labels[card_label]}')
#     try:
#         data_dir.mkdir()
#     except FileExistsError:
#         pass
#     man_url = 'https://www.lamoda.ru/' + man_card.find_next().get('href')
#     response_man_card = requests.get(man_url, headers=HEADERS)
#     soap_man_card = bs(response_man_card.text, 'html.parser')
#     man_card_images = soap_man_card.find_all('img')
#
#     for photo in man_card_images:
#         url_image = 'http:' + photo.get('src')
#         r = requests.get(url_image, headers=HEADERS)
#
#         with open(f'{str(data_dir).rstrip()}\\{picture_num}.jpg', "wb") as data_image:
#             data_image.write(r.content)
#         picture_num += 1
#     card_label += 1
#
# card_label = 0
# picture_num = 0
# for woman_card in woman_cards:
#     data_dir = Path(f'..\data\WOMEN\{woman_labels[card_label]}')
#     try:
#         data_dir.mkdir()
#     except FileExistsError:
#         pass
#     woman_url = 'https://www.lamoda.ru/' + woman_card.find_next().get('href')
#     response_woman_card = requests.get(woman_url, headers=HEADERS)
#     soap_woman_card = bs(response_woman_card.text, 'html.parser')
#     woman_card_images = soap_woman_card.find_all('img')
#
#     for photo in woman_card_images:
#         url_image = 'http:' + photo.get('src')
#         r = requests.get(url_image, headers=HEADERS)
#
#         with open(f'{str(data_dir).rstrip()}\\{picture_num}.jpg', "wb") as data_image:
#             data_image.write(r.content)
#         picture_num += 1
#     card_label += 1
