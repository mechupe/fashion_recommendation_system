import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options

# Headers to go to web
HEADERS = {
    'User-agent': '"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"'}
# Links of main page of clothes
main_link_woman = 'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/'
main_link_man = 'https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/'
# Categories we don't need to collect
invalid_categories = ['Одежда', 'Аксессуары', 'Premium', 'Красота', 'Спорт', 'Обувь', 'Одежда для беременных',
                      'Нижнее белье', 'Носки, чулки и колготки', 'Домашняя одежда',
                      'Одежда больших размеров', 'Плавки и шорты для плавания', 'Термобелье', 'Уход за одеждой',
                      'Купальники и пляжная одежда']


def selenium_parse(link):
    """Function, that goes to main page and
    parse html in order to take all categories links.

    :param link: clothes main page
    :return beautifulsoup page object

    """
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(link)
        time.sleep(5)
        return bs(driver.page_source, 'html.parser')
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def parse_page(gender, main_link, left_boundary, right_boundary, picture_num_start):
    """Function, which download clothes images from lamoda.ru
    in particular page range and categories.

    :param gender: Male or Female clothes and folder we download and create
    :param main_link: link of main lamoda men's/women's page
    :param left_boundary: left edge of range seacrh
    :param right_boundary: right edge of range seacrh
    :param picture_num_start: defines picture name in directory, if parser is stopped we start since
    the last picture num

    """
    categories = selenium_parse(main_link).find_all('a', class_='pPDgCAUDjSbGauRh05s9c')
    # Choose page number from range
    for page_number in range(left_boundary, right_boundary):
        for category in categories:
            try:
                if category.text not in invalid_categories:
                    # Go to category on needed page
                    clothes_url = 'https://www.lamoda.ru' + category.get('href') + '?page=' + str(page_number)
                    response = requests.get(clothes_url, headers=HEADERS, timeout=100)
                    soap = bs(response.text, 'html.parser')
                    cards = soap.find_all('div', class_='x-product-card__card')
                    labels_soap = soap.find_all('div', class_='x-product-card-description__product-name')
                    # Labels of clothes
                    labels = [label.text.split(' ')[1] for label in labels_soap]
                    card_label = 0
                    for card in cards:
                        data_dir = Path(f'..\data\{gender}\{labels[card_label]}')
                        try:
                            data_dir.mkdir()
                        except FileExistsError:
                            pass
                        # Go to card
                        url = 'https://www.lamoda.ru/' + card.find_next().get('href')
                        response_card = requests.get(url, headers=HEADERS)
                        soap_card = bs(response_card.text, 'html.parser')
                        card_images = soap_card.find_all('img')
                        # Download all photos from product's card
                        for photo in card_images:
                            url_image = 'http:' + photo.get('src')
                            r = requests.get(url_image, headers=HEADERS)

                            with open(f'{str(data_dir).rstrip()}\\{picture_num_start}.jpg', "wb") as data_image:
                                data_image.write(r.content)
                            picture_num_start += 1
                        card_label += 1
            except:
                print(f'Категория - {category}')
                print(f'Номер страницы - {page_number}')
                print(f'Номер картинки {picture_num_start}')
    print(picture_num_start)

# parse_page('MEN', main_link_man, left_boundary=101, right_boundary=200, picture_num_start=200000)
# parse_page('WOMEN', main_link_woman, left_boundary=1, right_boundary=100, picture_num_start=0)
