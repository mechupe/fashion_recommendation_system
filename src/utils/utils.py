import os
import shutil
import pandas as pd
from tqdm import tqdm
from PIL import Image

dir_name = r'C:\Users\79175\fashion_recommendation_system\data\Women'
class_1_path = r"C:\Users\79175\fashion_recommendation_system\data\Ростовые"
class_2_path = r"C:\Users\79175\fashion_recommendation_system\data\Неростовые"



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
    item_label_df.to_csv('item_label_df_1.csv')
    return item_label_df


def drop_duplicates(root_dir, threshold):
    classes_list = (quantity_inside_folder(root_dir, threshold)
                    .index[::-1])
    item_label_dict = {}
    for folder in tqdm(classes_list):
        for item in tqdm(os.listdir(dir_name + fr'\{folder}')):
            # item_series_num = item.split(' _')[0]
            if item in item_label_dict:
                os.remove(dir_name + fr'\{folder}' + fr'\{item}')
            else:
                item_label_dict[item] = folder


def to_8_bit(img_path):
    img = Image.open(img_path)
    img = img.convert('P', palette=Image.ADAPTIVE)
    # img = img.convert("RGB")
    # , palette=Image.ADAPTIVE, colors=8)
    img.save('8_bit_1.png')


def files_moving(folder, class_1_path, class_2_path, root_dir):
    for item in tqdm(os.listdir(root_dir + fr'\{folder}')):
        item_num = item.split('.')[0][-1]
        if item_num == '2':
            shutil.copy(root_dir + fr'\{folder}' + '\\' + item,
                        class_1_path)
        elif item_num == '1':
            shutil.copy(root_dir + fr'\{folder}' + '\\' + item,
                        class_2_path)


def separate_height_not_height_figures(root_dir):
    folders = os.listdir(root_dir)
    print(folders)
    for folder in tqdm(folders):
        if folder not in ['Комбинезон', 'Костюм', 'Футболка']:
            files_moving(folder=folder, class_1_path=class_1_path, class_2_path=class_2_path, root_dir=root_dir)
        elif folder in ['Комбинезон', 'Костюм']:
            files_moving(folder=folder, class_1_path=class_2_path, class_2_path=class_1_path, root_dir=root_dir)
        else:
            continue


# separate_height_not_height_figures(dir_name)
