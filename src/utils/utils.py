import os
import pandas as pd

dir_name = r'C:\Users\79175\fashion_recommendation_system\data\Women'


def quantity_inside_folder(root_dir):
    """Calculate dataframe with folders names and elements quantity in them
    :param root_dir: directory when all folders are located
    :return df: dataframe with two cols - folders names and elements quantity in them
    """
    folders = os.listdir(root_dir)
    dict_cat_count = {}

    for folder in folders:
        dict_cat_count[folder] = len(os.listdir(dir_name + f'\{folder}'))

    df = (
        pd.DataFrame.from_dict(dict_cat_count, orient='index')
        .rename(columns={0: 'count_files'})
        .sort_values(by='count_files', ascending=False)
    )
    return df

