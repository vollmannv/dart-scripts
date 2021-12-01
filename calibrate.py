from camera import Camera
import processing
import json


def calibrate(list_of_cameras):
    input("Please remove all darts from the board and press enter.")
    for camera in list_of_cameras:
        camera.setControlImage()
    input("Please place a dart in bullseye and press enter.")
    for camera in list_of_cameras:
        camera.differences()
        x_coord = processing.process_image(camera.diff_frame)
        data = {}
        data['camera' + str(camera.index)] = []
        data['camera' + str(camera.index)].append({
            'center': str(x_coord)
        })
        out = open("camera-calibrations.json", "w")
        json.dump(data, out)
        out.close()


if __name__ == '__main__':
    cam1 = Camera(1)
    cam2 = Camera(2)
    cams = [cam1, cam2]
    calibrate(cams)
