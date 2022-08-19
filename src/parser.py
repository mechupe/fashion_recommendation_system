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
men_clothes_url = f'https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3&page={1}'
women_clothes_url = f'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?page={1}'
response_man = requests.get(men_clothes_url, headers=HEADERS, timeout=1000)
response_woman = requests.get(women_clothes_url, headers=HEADERS)

soap_man = bs(response_man.text, 'html.parser')
soap_woman = bs(response_woman.text, 'html.parser')

types = soap_man.find_all(class_='x-product-card-description__product-name')
links = soap_man.find_all('img')
print(links)
i = 0
for link in links:
    i+=1
    url = link.get('src')
    r = requests.get('http:' + url, headers=HEADERS)
    out = open(f"..\data\{i}.jpg", "wb")
    out.write(r.content)
    out.close()