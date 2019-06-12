# from ctypes import c_uint16
from pymavlink import mavutil

# def setAttitude(ml, sem, roll, pitch, yaw, rollSpeed=30, pitchSpeed=30, yawSpeed=30):
#     try:
#         ml.mav.command_long_send(
#             ml.target_system,
#             ml.target_component,
#             mavutil.mavlink.MAV_CMD_CONDITION_YAW,
#             0,  # Confirmation
#             angle,  # param1: target angle (deg)
#             rate,  # param2: angular speed (deg/s)
#             direction,  # param3: direction (-1=ccw, 1=cw)
#             relative,  # param4: 0 = absolute, 1 = relative
#             0,  # param5: Meaningless
#             0,  # param6: Meaningless
#             0)  # param7: Meaningless
#     finally:
#         sem.release()


def changeAltitude(ml, sem, rate, altitude):
    try:
        print("Moving to altitude " + str(altitude) + " at " + str(rate) + " m/s.")

        ml.mav.command_long_send(
            ml.target_system,
            ml.target_component,
            mavutil.mavlink.MAV_CMD_CONDITION_CHANGE_ALT,
            0,  # Confirmation
            rate,  # param1: ascent/descent rate (m/s)
            0,  # param2: Empty
            0,  # param3: Empty
            0,  # param4: Empty
            0,  # param5: Empty
            0,  # param6: Empty
            altitude)  # param7: Finish Altitude
    finally:
        sem.release()

def lightsMax(ml, sem):
    try:
        print("Setting lights to max")
        ml.set_servo(9, 1900)

    finally:
        sem.release()

def lightsoff(ml, sem):
    try:
        print("Setting lights to off")
        ml.set_servo(9, 1900)
    finally:
        sem.release()

# def changeAltitude(ml, sem, rate, altitude):
#     try:
#         ml.mav.command_long_send(
#             ml.target_system,
#             ml.target_component,
#             mavutil.mavlink.MAV_CMD_CONDITION_CHANGE_ALT,
#             0,  # Confirmation
#             rate,  # param1: ascent/descent rate (m/s)
#             0,  # param2: Empty
#             0,  # param3: Empty
#             0,  # param4: Empty
#             0,  # param5: Empty
#             0,  # param6: Empty
#             altitude)  # param7: Finish Altitude
#     finally:
#         sem.release()

# MAV_CMD_DO_CHANGE_ALTITUDE
# MAV_CMD_REQUEST_CAMERA_INFORMATION
