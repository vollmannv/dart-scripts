from camera import Camera
import processing
import json


def calibrate(list_of_cameras):
    input("Please remove all darts from the board and press enter.")
    for camera in list_of_cameras:
        camera.setControlImage()
    input("Please place a dart in bullseye and press enter.")
    data = {}

    for camera in list_of_cameras:
        camera.differences()
        x_coord = processing.process_calibration(camera.diff_frame)
        data['camera' + str(camera.index)] = {'center': str(x_coord)}

    out = open("camera-calibrations.json", "w")
    json.dump(data, out)
    out.close()


if __name__ == '__main__':
    cam1 = Camera(1)
    cam2 = Camera(2)
    cam3 = Camera(3)
    cam4 = Camera(4)
    cams = [cam1, cam2, cam3, cam4]
    calibrate(cams)
