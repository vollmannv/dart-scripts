import cv2
import time
import json
import numpy as np


def process_image(img):
    img = amplify_contrast(img)
    indices = np.where(img == [255])
    print(indices[0])
    highest = [0, 0]
    for i in range(len(indices[0])):
        if indices[0][i] >= highest[0]:
            highest = [indices[0][i], indices[1][i]]
    print(highest[1])
    processedimg = np.zeros((60,640,3), np.uint8)
    cv2.line(processedimg, (highest[1], 0), (highest[1], 60), (0,255,0), 1)
    cv2.line(processedimg, (320, 0), (320, 60), (0, 0, 255), 1)
    cv2.imshow('final', processedimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return(highest[1])

def amplify_contrast(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray = cv2.threshold(gray,127,255,0)
    gray2 = gray.copy()
    mask = np.zeros(gray.shape,np.uint8)
    cv2.bitwise_not(gray2,gray2,mask)
    cv2.fastNlMeansDenoising(gray2, gray2)
    return gray2

def measure_distance(x_coord, camera):
    with open('camera-calibrations.json') as f:
        data = json.load(f)
    center_coord = data['camera' + str(camera.index)]['center']

    return absdiff(x_coord, center_coord)
