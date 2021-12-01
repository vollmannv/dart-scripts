import camera
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
            'center': x_coord
        })
        json.dump(data, 'camera-calibrations.json')
