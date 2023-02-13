import os
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from tqdm import tqdm
import numpy as np
from selenium.common.exceptions import NoSuchWindowException

# Headers to go to web
HEADERS = {
    'User-agent': '"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"'}
# Link of main page of clothes
main_link_woman = 'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/'
# Categories we don't need to collect
invalid_categories = ['Одежда', 'Аксессуары', 'Premium', 'Красота', 'Спорт', 'Обувь', 'Одежда для беременных',
                      'Нижнее белье', 'Носки, чулки и колготки', 'Домашняя одежда',
                      'Одежда больших размеров', 'Плавки и шорты для плавания', 'Термобелье', 'Уход за одеждой',
                      'Купальники и пляжная одежда']


def element_click(driver, num_clicks, link_text):
    driver.execute_script("window.scrollTo(0, 1700)")
    for _ in range(num_clicks):
        time.sleep(2)
        element = driver.find_element(By.LINK_TEXT, link_text).click()

def selenium_parse(link, uncover=False):
    """Function, that goes to main page and
    parse html in order to take all categories links.

    :param link: clothes main page
    :return beautifulsoup page object

    """
    options = Options()
    options.headless = True
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    try:
        driver.get(link)
        if uncover:
            time.sleep(2)
            link_text = 'Подробнее'
            num_elements = len(driver.find_elements(By.LINK_TEXT, link_text))
            element_click(driver=driver, num_clicks=num_elements-1, link_text=link_text)
        return bs(driver.page_source, 'html.parser')
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def parse_page(gender, main_link, left_boundary, right_boundary):
    """Function, which download clothes images from lamoda.ru
    in particular page range and categories.

    :param gender: Male or Female clothes and folder we download and create
    :param main_link: link of main lamoda men's/women's page
    :param left_boundary: left edge of range seacrh
    :param right_boundary: right edge of range seacrh
    :param picture_num_start: defines picture name in directory, if parser is stopped we start since
    the last picture num

    """
    # Particular classes of the categories on left panel
    categories = selenium_parse(main_link).find_all('a', class_='_root_clp6c_2 _label_clp6c_17 _link_ki68p_27 _link_ki68p_27')
    json_list = []
    # Choose page number from range
    for page_number in tqdm(range(left_boundary, right_boundary)):
        for category in tqdm(categories):
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
                for card in tqdm(cards):
                    data_dir = f'..\..\data\{gender}\{labels[card_label]}'
                    if not os.path.exists(data_dir):
                        os.makedirs(data_dir)
                    # Go to card
                    url = 'https://www.lamoda.ru/' + card.find_next().get('href')
                    try:
                        card_info = selenium_parse(url, uncover=True)

                        if card_info:
                            card_images = card_info.find_all('img', class_='_root_1wiwn_3 _image_uhouy_54 _image_uhouy_54')

                            card_metainfo = card_info.find_all('span', class_='_attributeName_ajirn_14')
                            card_metainfo_data = card_info.find_all('span', class_='_value_ajirn_27')
                            metainfo_dict = {key.text: value.text for key, value in zip(card_metainfo, card_metainfo_data)}
                            card_description = card_info.find('div', class_='_description_1ga1h_20')
                        else:
                            with open('..\..\data\logger.txt', 'a') as file:
                                msg = f"{url} hasn't been parsed\n"
                                file.write(msg)
                                continue
                        try:
                            card_subclass = card_info.find_all('a', class_='_root_clp6c_2 _secondaryLabel_clp6c_13')[-1].text
                            metainfo_dict['card_subclass'] = card_subclass
                        except IndexError:
                            metainfo_dict['card_subclass'] = np.nan

                        if card_description:
                            metainfo_dict['description'] = card_description.find_next().text

                        json_list.append(metainfo_dict)
                        with open('..\..\data\metainfo_2.json', 'w', encoding='utf-8') as file:
                            metainfo_dict_json = json.dump(json_list,
                                                           file,
                                                           ensure_ascii=False)
                        # Download all photos from product's card
                        photo_num = 1
                        for photo in card_images[:2]:

                            url_image = 'http:' + photo.get('src')
                            r = requests.get(url_image, headers=HEADERS)

                            with open(f'{str(data_dir).rstrip()}\\{metainfo_dict["Артикул"]}_{photo_num}.jpg', "wb") as data_image:
                                data_image.write(r.content)
                            photo_num += 1
                        card_label += 1
                    except NoSuchWindowException:
                        with open('..\..\data\logger.txt', 'a') as file:
                            msg = f"{url} hasn't been parsed\n"
                            file.write(msg)
                        continue





# categories = selenium_parse(main_link_woman).find_all('a', class_='_root_clp6c_2 _label_clp6c_17 _link_ki68p_27 _link_ki68p_27')
# for category in categories:
#     print(category.get('href'))
# print(len(categories))
parse_page('Women', main_link_woman, left_boundary=1, right_boundary=100)