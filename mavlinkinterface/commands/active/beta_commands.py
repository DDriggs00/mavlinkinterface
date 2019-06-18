# from ctypes import c_uint16
from pymavlink import mavutil
from time import sleep
import logging

from mavlinkinterface.commands.passive.pressure import getDepth

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

def lightsMax1(ml, sem):
    try:
        print("Setting lights to max")
        ml.set_servo(9, 1900)

    finally:
        sem.release()

def lightsoff1(ml, sem):
    try:
        print("Setting lights to off")
        ml.set_servo(9, 1100)
    finally:
        sem.release()

def lightsUp(ml, sem):
    try:
        buttons = 1 << 14
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.1)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        sem.release()

def lightsDown(ml, sem):
    try:
        buttons = 1 << 14
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.25)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        sem.release()

def gripperClose(ml, sem):
    try:
        buttons = 1 << 9
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.25)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        sem.release()

def gripperOpen(ml, sem):
    try:
        buttons = 1 << 10
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.25)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        sem.release()

# def changeAltitude(ml, sem, rate, altitude):
#     try:
#         ml.mav.command_long_send(
#             ml.target_system,
#             ml.target_component,
#             mavutil.mavlink.SET_ATTITUDE_TARGET,
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

def diveDepth(ml, sem, depth, throttle=100, absolute=False):
    '''
    :param depth: The change in depth, negative being down
    :param throttle: Percent of thruster power to use
    '''
    try:
        print("Diving at " + str(throttle) + "% throttle by " + str(depth) + " m")
        print("DiveDepth depth=" + str(depth) + ", throttle=" + str(throttle) + " absolute=" + str(absolute))
        currentDepth = getDepth(ml)

        if absolute:
            # In absolute mode, just go to a depth
            targetDepth = depth
        else:
            # In relative mode, go up/down by a depth
            targetDepth = depth + currentDepth
        if targetDepth > 0:
            logging.info("Cannot Rise above the Surface, aborting")
            raise ValueError("Cannot Rise above the Surface, aborting command")
        i = 0
        oldDepth = currentDepth
        stuck = False
        # If the drone is below the desired depth
        if currentDepth > targetDepth:     # Need to Dive
            z = (throttle * 5) + 500 * -1
            while currentDepth > targetDepth + .5 and not stuck:     # Until within 1.5m of target, thrust at desired throttle
                currentDepth = getDepth(ml)
                ml.mav.manual_control_send(
                    ml.target_system,
                    0,  # x [ forward(1000)-backward(-1000)]
                    0,  # y [ left(-1000)-right(1000) ]
                    z,  # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
                    0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
                    0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
                if i == 30:                                 # If, over the course 5 sec
                    if -1 <= oldDepth - currentDepth <= 1:  # If depth has not changed
                        stuck = True                        # The drone must either be stuck or at the surface, but miscalibrated
                    i = 0
                    oldDepth = currentDepth
                i += 1
                sleep(0.1)
        # If the drone is below the desired depth
        elif currentDepth < targetDepth:
            z = (throttle * 5) + 500
            while currentDepth < targetDepth + .5 and not stuck:     # Until within 1.5m of target, thrust at desired throttle
                currentDepth = getDepth(ml)
                ml.mav.manual_control_send(
                    ml.target_system,
                    0,  # x [ forward(1000)-backward(-1000)]
                    0,  # y [ left(-1000)-right(1000) ]
                    z,  # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
                    0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
                    0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
                if i == 30:                                 # If, over the course 5 sec
                    if -1 <= oldDepth - currentDepth <= 1:  # If depth has not changed
                        stuck = True                        # The drone must either be stuck or at the surface, but miscalibrated
                    i = 0
                    oldDepth = currentDepth
                i += 1
                sleep(0.1)

        # Stop thrusting when the desired depth has been reached
        ml.mav.manual_control_send(
            ml.target_system,
            0,      # x [ forward(1000)-backward(-1000)]
            0,      # y [ left(-1000)-right(1000) ]
            500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
            0,      # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        sem.release()
