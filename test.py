import cv2
from camera import Camera

if __name__ == '__main__':
    for i in range(0, 5):
        cam = Camera(i)
        res, frame = cam.camera.read()
        cv2.imwrite("cam" + str(i) + ".jpg", frame)