import math

import cv2, time, pandas as pd
from datetime import datetime
from multiprocessing import Process
import processing

list_of_cameras = []


class Camera:

    def __init__(self, index):
        self.index = index
        self.camera = cv2.VideoCapture(index)
        self.imct = 0
        self.thresh_frame = None
        self.diff_frame = None
        self.gray = None
        self.control_image = None
        self.motion = 0
        self.currentval = 0

    def setControlImage(self):
        s, img = self.camera.read()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        self.control_image = img[340:400, 0:640]

    def take_picture(self):
        if self.imct < 10:
            s, img = self.camera.read()
            if s:
                img = img[340:400, 0:640]
                time = datetime.now()
                time = time.strftime("%Y-%m-%d_%H-%M-%S")
                path = "camera" + str(self.index) + "_" + time + ".jpg"
                if not cv2.imwrite(path, self.diff_frame):
                    raise Exception("could not save")
                self.imct += 1
                print("image saved to: " + path)
            else:
                print("didnt work")

    def monitor(self, cameras):

        check, frame = self.camera.read()

        self.motion = 0.0

        frame = frame[340:400, 0:640]

        self.gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        self.diff_frame = cv2.absdiff(self.control_image, self.gray)
        self.thresh_frame = cv2.threshold(self.diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        self.thresh_frame = cv2.dilate(self.thresh_frame, None, iterations=2)

        cnts, _ = cv2.findContours(self.thresh_frame.copy(),
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < 400:
                continue
            self.motion = 1
            (x, y, w, h) = cv2.boundingRect(contour)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if self.motion == 1:
            for cam in cameras:
                cam.differences()
                #cam.take_picture()
                cam.setControlImage()
                cam.currentval = processing.process_image(cam.diff_frame, cam.index)
            process_images()
            self.motion = 0
            self.control_image = self.gray

    def differences(self):
        check, frame = self.camera.read()
        frame = frame[340:400, 0:640]
        self.gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        self.diff_frame = cv2.absdiff(self.control_image, self.gray)


def process_images():
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    for cam in list_of_cameras:
        if cam.index == 2:              #Links
            y1 = cam.currentval * -1
        elif cam.index == 1:            #Unten
            x1 = cam.currentval
        elif cam.index == 3:            #Oben
            x2 = cam.currentval * -1
        else:                           #Rechts
            y2 = cam.currentval

    x_coord = (x1 + x2) / 2
    y_coord = (y1 + y2) / 2

    if x_coord == 0 or y_coord == 0:
        return

    angle = math.degrees(math.atan2(y_coord, x_coord))
    if angle < 0:
        angle = angle + 360
    print(str("x: " + str(x_coord) + ", y: " + str(y_coord) + ", angle: " + str(angle)))
    print("x1: " + str(x1) + ", x2: " + str(x2) + ", y1: " + str(y1) + ", y2: " + str(y2))

    distanceToMiddle = math.dist([x_coord, y_coord], [0, 0])
    print(distanceToMiddle)
    double1 = 1  #where the "double" area starts, from the middle
    double2 = 2  #where the "double" area end, from the middle
    tripple1 = 1  #where the "tripple" area starts
    tripple2 = 2  #where the "tripple" area ends

    def printvalue(val):
        if double1 <= distanceToMiddle <= double2:
            print("2 * " + str(val))
        elif tripple1 <= distanceToMiddle <= tripple2:
            print("3 * " + str(val))
        else:
            print(val)

    if 9 <= angle < 27:
        printvalue(13)
    elif 27 <= angle < 45:
        printvalue(4)
    elif 45 <= angle < 63:
        printvalue(18)
    elif 63 <= angle < 81:
        printvalue(1)
    elif 81 <= angle < 99:
        printvalue(20)
    elif 99 <= angle < 117:
        printvalue(5)
    elif 117 <= angle < 135:
        printvalue(12)
    elif 135 <= angle < 153:
        printvalue(9)
    elif 153 <= angle < 171:
        printvalue(14)
    elif 171 <= angle < 189:
        printvalue(11)
    elif 189 <= angle < 207:
        printvalue(8)
    elif 207 <= angle < 225:
        printvalue(16)
    elif 225 <= angle < 243:
        printvalue(7)
    elif 243 <= angle < 261:
        printvalue(19)
    elif 261 <= angle < 279:
        printvalue(3)
    elif 279 <= angle < 297:
        printvalue(17)
    elif 297 <= angle < 315:
        printvalue(2)
    elif 315 <= angle < 333:
        printvalue(15)
    elif 333 <= angle < 351:
        printvalue(10)
    else:
        print(6)


if __name__ == '__main__':
    cam1 = Camera(1)
    cam2 = Camera(2)
    cam3 = Camera(3)
    cam4 = Camera(4)
    list_of_cameras.append(cam1)
    list_of_cameras.append(cam2)
    list_of_cameras.append(cam3)
    list_of_cameras.append(cam4)

    for cam in list_of_cameras:
        cam.setControlImage()

    print("GOOOOO!")

    while (True):
        cam3.monitor(list_of_cameras)
        time.sleep(0.6)
        cam2.monitor(list_of_cameras)
        time.sleep(0.6)
