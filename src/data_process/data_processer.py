import os
from collections import Counter
import cv2
import json
import re
import numpy as np

# Find background colors
background_threshold = 40


def count_colors(image_path) -> Counter:
    """Count pixels of the image.

    :param image_path: path of the image
    :type image_path: str

    :return: colors_count, Counter dict with counts of each pixel count in image
    """
    image = cv2.imread(image_path)
    # Splits image Mat into 3 color channels in individual 2D arrays
    (channel_b, channel_g, channel_r) = cv2.split(image)

    # Flattens the 2D single channel array so as to make it easier to iterate over it
    channel_b = channel_b.flatten()
    channel_g = channel_g.flatten()
    channel_r = channel_r.flatten()
    rgb_list = list()
    for i in range(len(channel_b)):
        pixel_rgb = (channel_r[i], channel_g[i], channel_b[i])
        rgb_list.append(pixel_rgb)
    colors_count = Counter(rgb_list)
    return colors_count


def percentile_colors(image_path) -> list:
    """Create list of most_common pixels in image.

    :param image_path: path of the image
    :type image_path: str

    :return: majority_pixels, list of (r ,g, b) channels of most common pixels im image
    """
    counts_colors = count_colors(image_path).most_common()
    # Create separate list only with counts of pixels
    counts = [count[1] for count in counts_colors]
    # Transform values from counts list to list of percents
    perc_counts = [count / sum(counts) for count in counts]

    iterator = 0
    summator = 0

    for percent in perc_counts:
        if summator < background_threshold:
            summator += percent * 100
            iterator += 1
        else:
            majority_pixels = [rgb for rgb, count in counts_colors[:iterator]]
            return majority_pixels


def background_pixels_define(data_path, threshold):
    """Find all images in directory and save most common pixels of each image in file

    :param data_path: path to folders with sex and categories
    :type data_path: str
    :param threshold: how many percent of image background may be (configured)
    :type threshold: int
    """
    os.chdir(data_path)
    # We count images in order to stop loop when limit the threshold
    counter = 0
    man_woman = os.listdir(os.getcwd())
    most_pixels = list()
    # Go to dir with folders MEN WOMEN
    for sex in man_woman:
        sex_path = os.getcwd()
        os.chdir(sex_path + f'\\{sex}')
        categories = os.listdir(os.getcwd())
        # Go to category of clothes
        for category in categories:
            categories_path = os.getcwd()
            os.chdir(categories_path + f'\\{category}')
            images = os.listdir(os.getcwd())
            # Go to image
            for image in images:
                most_pixels.extend(percentile_colors(image_path=image))
                counter += 1
                print(f'{threshold - counter} files left')
                # Break if hit threshold
                if counter > threshold:
                    break
            if counter > threshold:
                # Reset counter and go to the next gender dir
                counter = 0
                break
            os.chdir(categories_path)
        os.chdir(sex_path)
    # Count most common pixels and save info to the file
    backgrounds = Counter(most_pixels)
    with open('backgrounds.json', 'w') as file:
        backgrounds = {str(k): backgrounds[k] for k in backgrounds}
        backgrounds_js = json.dumps(backgrounds)
        json.dump(backgrounds_js, file)
    with open('pixels_percentage.json', 'w') as f:
        background_perc_dict = {key: value / sum(backgrounds.values()) for key, value in backgrounds.items()}
        pixels_perc = json.dumps(background_perc_dict)
        json.dump(pixels_perc, file)


if __name__ == "__main__":
    with open('pixels_percentage.json') as f:
        pix_perc_str = json.load(f)
        pix_perc_dict = json.loads(pix_perc_str)
        pix_perc_dict = dict(sorted(pix_perc_dict.items(), key=lambda item: item[1], reverse=True))

        iterator = 0
        summator = 0

        for pixel, count in pix_perc_dict.items():
            if summator < background_threshold:
                summator += count * 100
                iterator += 1
            else:
                background_pixels = []
                for pixel, part in list(pix_perc_dict.items())[:iterator]:
                    rgb = list(map(lambda x: int(x), re.findall(r'\d+', pixel)))
                    if sum(np.array(rgb) >= 220) == 3:
                        rgb_list = pixel.split(',')
                        pixel = list(map(int, [rgb_list[0][1:], rgb_list[1][1:], rgb_list[2][1:-1]]))
                        background_pixels.append(pixel)
                break


    # print([(int(i[1:]), int(x), int(j[:-1])) for i, x, j in '(233, 233, 233)'.split(' ,')])
    # print('(233, 233, 233)'.split(','))

if __name__ == '__main__':
    print(percentile_colors('17357.jpg'))
#     src = cv2.imread('3757.jpg')
#     b, g, r = cv2.split(src)
#
#     cv2.imshow('image', src)
#     cv2.waitKey(0)
# image1 = face_recognition.load_image_file("3540.jpg")
# face_locations = face_recognition.face_locations(image1)
# width, height =0,0
# if face_locations:
#     for face_location in face_locations:
#         top, right, bottom, left = face_location
#         face_image = image1[bottom+20:, :]
#         img = Image.fromarray(face_image, 'RGB')
#         # img.save('my.png')
#         img.show()
# else:
#     img = Image.fromarray(image1, 'RGB')
#     # img.save('my.png')
#     img.show()
