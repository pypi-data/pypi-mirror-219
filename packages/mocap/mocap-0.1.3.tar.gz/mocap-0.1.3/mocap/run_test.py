from .ArucoHelper import ArucoHelper


def run_test(camera_id=0, track_tag=None, duration=-1):
    if track_tag is None:
        track_tag = [1]
    if not isinstance(track_tag, list):
        track_tag = [track_tag]
    # camera id could be 1 if there is another one
    a = ArucoHelper(camera_id=camera_id)
    # init_camera tries to read calibration data
    a.init_camera()
    #a.calibrate(0.02)
    a.run(track_tag, duration=duration)


