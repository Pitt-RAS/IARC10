import cv2
import pyrealsense2 as rs
import numpy as np
import math


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 250)
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)

profile = pipeline.start(config)

def get_gyro_data(gyro):
    return np.asanyarray([gyro.x, gyro.y, gyro.z])

def get_accel_data(accel):
    return np.asanyarray([accel.x, accel.y, accel.z])

while True:
    frame = pipeline.wait_for_frames()
    gyro = get_gyro_data(frame[0].as_motion_frame().get_motion_data())
    accel = get_accel_data(frame[0].as_motion_frame().get_motion_data())
    print('accelerometer', accel)
    print('gyroscope', gyro)



