import cv2
import time
import json
import numpy as np


def process_image(img, index):
    calibrations = open("camera-calibrations.json", "r")
    data = json.load(calibrations)
    offset = data["camera" + str(index)]["center"]
    img = amplify_contrast(img)
    indices = np.where(img == [255])
    highest = [0, 0]
    for i in range(len(indices[0])):
        if indices[0][i] >= highest[0]:
            highest = [indices[0][i], indices[1][i]]
    return highest[1] - 320 + int(offset)


def process_calibration(img):
    img = amplify_contrast(img)
    indices = np.where(img == [255])
    highest = [0, 0]
    for i in range(len(indices[0])):
        if indices[0][i] >= highest[0]:
            highest = [indices[0][i], indices[1][i]]
    return highest[1] - 320


def amplify_contrast(img):
    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, gray = cv2.threshold(img, 127, 255, 0)
    gray2 = gray.copy()
    mask = np.zeros(gray.shape, np.uint8)
    cv2.bitwise_not(gray2, gray2, mask)
    cv2.fastNlMeansDenoising(gray2, gray2)
    return gray2


def measure_distance(x_coord, camera):
    with open('camera-calibrations.json') as f:
        data = json.load(f)
    center_coord = data['camera' + str(camera.index)]['center']

    return abs(x_coord - center_coord)
