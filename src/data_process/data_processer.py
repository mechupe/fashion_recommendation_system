import os
from collections import Counter
import cv2
import json

# Find background colors
background_threshold = 40


def count_colors(image_path):
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


def percentile_colors(image_path):
    counts_colors = count_colors(image_path).most_common()
    counts = [count[1] for count in counts_colors]
    perc_counts = [count / sum(counts) for count in counts]

    iterator = 0
    summator = 0

    for percent in perc_counts:
        if summator < background_threshold:
            summator += percent * 100
            iterator += 1
        else:
            return [rgb for rgb, count in counts_colors[:iterator]]


def background_pixels_define(data_path, threshold, ):

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
            categoties_path = os.getcwd()
            os.chdir(categoties_path + f'\\{category}')
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
            os.chdir(categoties_path)
        os.chdir(sex_path)
    # Count most common pixels and save info to the file
    backgrounds = Counter(most_pixels)
    with open('backgrounds.json', 'w') as file:
        backgrounds = json.dumps({str(k): backgrounds[k] for k in backgrounds})
        json.dump(backgrounds, file)


#if __name__ == "__main__":


# if __name__ == '__main__':
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
