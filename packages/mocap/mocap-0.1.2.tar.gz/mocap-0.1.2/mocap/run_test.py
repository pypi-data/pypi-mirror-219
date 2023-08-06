from ArucoHelper import ArucoHelper


# camera id could be 1 if there is another one
a = ArucoHelper(camera_id=0)
# init_camera tries to read calibration data
a.init_camera()
#a.calibrate(0.02)
a.run([3,2,1])
