import sys
from collections import Counter
import cv2
import numpy as np
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary
import face_recognition
import cloudinary.api
import matplotlib.pyplot as plt
from PIL import Image
import json

# Find background colors
threshhold = 40


def count_colors(image_path):
    image = cv2.imread(image_path)
    # Splits image Mat into 3 color channels in individual 2D arrays
    (channel_b, channel_g, channel_r) = cv2.split(image)

    # Flattens the 2D single channel array so as to make it easier to iterate over it
    channel_b = channel_b.flatten()
    channel_g = channel_g.flatten()  # ""
    channel_r = channel_r.flatten()  # ""
    rgb_list = list()
    for i in range(len(channel_b)):
        pixel_rgb = (channel_r[i], channel_g[i], channel_b[i])
        rgb_list.append(pixel_rgb)
    colors_count = Counter(rgb_list)
    return colors_count


def percentile_colors(image_path):
    counts_colors = count_colors(image_path).most_common()

    counts = [count[1] for count in counts_colors]
    print(counts)
    perc_counts = [count / sum(counts) for count in counts]

    iterator = 0
    summator = 0
    for percent in perc_counts:
        if summator < threshhold:
            summator += percent * 100
            iterator += 1
        else:
            return [rgb for rgb, count in counts_colors[:iterator]]

if __name__ == "__main__":
    print(percentile_colors('17357.jpg'))

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
