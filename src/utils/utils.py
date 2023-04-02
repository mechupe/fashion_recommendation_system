import os
import pandas as pd
from tqdm import tqdm
from PIL import Image


dir_name = r'C:\Users\79175\fashion_recommendation_system\data\Women'


def quantity_inside_folder(root_dir, threshold=None):
    """Calculate dataframe with folders names and elements quantity in them
    :param root_dir: directory when all folders are located
    :return df: dataframe with two cols - folders names and elements quantity in them
    """
    folders = os.listdir(root_dir)
    dict_cat_count = {}

    for folder in folders:
        dict_cat_count[folder] = len(os.listdir(dir_name + fr'\{folder}'))

    df = (
        pd.DataFrame.from_dict(dict_cat_count, orient='index')
        .rename(columns={0: 'count_files'})
        .sort_values(by='count_files', ascending=False)
    )

    if threshold:
        df = df.query(f'count_files >= {threshold}')

    return df


def file_to_label(root_dir):
    folders = os.listdir(root_dir)
    item_label_df = pd.DataFrame(columns=['Артикул', 'Class'])

    for folder in tqdm(folders):
        for item in tqdm(os.listdir(dir_name + fr'\{folder}')):
            item_label_row = pd.DataFrame({'Артикул': [item.split(' _')[0]], 'Class': [folder]})
            item_label_df = pd.concat([item_label_df, item_label_row])
    item_label_df.to_csv('item_label_df.csv')
    return item_label_df


def drop_duplicates(root_dir, threshold):
    classes_list = (quantity_inside_folder(root_dir, threshold)
                    .index[::-1])
    item_label_dict = {}
    for folder in tqdm(classes_list):
        for item in tqdm(os.listdir(dir_name + fr'\{folder}')):
            item_series_num = item.split(' _')[0]
            if item_series_num in item_label_dict:
                os.remove(dir_name + fr'\{folder}' + fr'\{item}')
            else:
                item_label_dict[item_series_num] = folder


def to_8_bit(img_path):
    img = Image.open(img_path)
    img = img.convert('P', palette=Image.ADAPTIVE)
    # img = img.convert("RGB")
                      # , palette=Image.ADAPTIVE, colors=8)
    img.save('8_bit_1.png')

to_8_bit('MP002XW0C77R _1.jpg')