from rems.robots.RobotBase import RobotBase
from .ArucoDevice import ArucoDevice
from .timestamp import time_str



class ArucoBot(RobotBase):
    DEVICE_LIST = [ArucoDevice]
    def __init__(self, tracids=None, camera_id=0, filename=None, env=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run.DT = 0.1
        self.run.name = 'Aruco'
        self.run.supress_info = False
        self.tracids = tracids
        self.camera_id = camera_id
        if filename is None:
            filename = f'video/aruco_{time_str()}.avi'
        self.aruco = ArucoDevice(track_id=self.tracids, camera_id=self.camera_id, video_name=filename,
                        dt=self.run.DT, env=env)
        self.add_device(self.aruco)

    def define(self, *args, **kwargs):
        self.state = self.aruco.aruco_state
        super().define()



