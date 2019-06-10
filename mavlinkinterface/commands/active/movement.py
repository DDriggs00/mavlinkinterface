from time import sleep
from pymavlink import mavutil

def move3d(ml, sem, time, throttleX, throttleY, throttleZ):
    '''Throttle functions are integers from -100 to 100'''
    try:
        print("Moving in direction X=" + str(throttleX) + " Y=" + str(throttleY) + " Z=" + str(throttleZ) + " for " + str(time) + " seconds")
        x = 10 * throttleX
        y = 10 * throttleY
        z = 5 * throttleZ + 500
        for i in range(0, time * 4):
            ml.mav.manual_control_send(
                ml.target_system,
                x,  # x [back(-1000), forward(1000)]
                y,  # y [left(-1000), right(1000)]
                z,  # z [down(0), up(1000)]
                0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
                0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
            sleep(.25)
        ml.mav.manual_control_send(
            ml.target_system,
            0,  # x [back(-1000), forward(1000)]
            0,  # y [left(-1000), right(1000)]
            500,  # z [down(0), up(1000)]
            0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]

    finally:
        sem.release()

def move(ml, sem, direction, time, throttle=100):
    '''
    Modes the sub in 2 dimensions
    :param direction: The angle (from -180 to 180) to move the sub at
    '''
    try:
        print("Moving in direction: " + str(direction) + " at " + str(throttle) + "% throttle for " + str(time) + " seconds")
        x = y = 0
        if direction == "forward" or direction == 0:
            x = 10 * throttle
        elif direction == "back" or direction == 180 or direction == -180:
            x = -10 * throttle
        elif direction == "left" or direction == -90:
            y = -10 * throttle
        elif direction == "right" or direction == -90:
            y = 10 * throttle

        for i in range(0, (time * 4)):
            ml.mav.manual_control_send(
                ml.target_system,
                x,      # x [ forward(1000)-backward(-1000)]
                y,      # y [ left(-1000)-right(1000) ]
                500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
                0,      # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
                0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
            sleep(.25)
        ml.mav.manual_control_send(
            ml.target_system,
            0,      # x [ forward(1000)-backward(-1000)]
            0,      # y [ left(-1000)-right(1000) ]
            500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
            0,      # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]

    finally:
        sem.release()

def moveAbsolute(ml, sem, direction, time, throttle=100):  # TODO
    # TODO: insert movement code here
    try:
        sleep(5)
    finally:
        sem.release()

def dive(ml, sem, time, throttle):
    '''
    :param time: the number of seconds to power the thrusters
    :param throttle: Throttle value is from -100 to 100, with negative indicating down
    '''
    try:
        print("Diving at " + str(throttle) + "% throttle for " + str(time) + "seconds")
        z = (throttle * 5) + 500
        for i in range(0, (time * 4)):
            ml.mav.manual_control_send(
                ml.target_system,
                0,  # x [ forward(1000)-backward(-1000)]
                0,  # y [ left(-1000)-right(1000) ]
                z,  # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
                0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
                0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
            sleep(0.25)
        ml.mav.manual_control_send(
            ml.target_system,
            0,  # x [ forward(1000)-backward(-1000)]
            0,  # y [ left(-1000)-right(1000) ]
            500,  # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
            0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        sem.release()

def diveAbsolute(ml, sem, depth):  # TODO
    # TODO: insert movement code here
    try:
        sleep(5)
    finally:
        sem.release()

def surface(ml, sem):  # TODO
    # TODO: insert movement code here
    try:
        sleep(5)
    finally:
        sem.release()

def yaw(ml, sem, angle, rate=20, direction=1, relative=0):
    try:
        print("Yawing " + ("clockwise by " if (direction == 1) else "Counterclockwise by ") + str(angle) + " degrees at " + str(rate) + " deg/s in " + ("relative" if (relative == 1) else "Absolute") + " mode.")

        ml.mav.command_long_send(
            ml.target_system,
            ml.target_component,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,
            0,  # Confirmation
            angle,  # param1: target angle (deg)
            rate,  # param2: angular speed (deg/s)
            direction,  # param3: direction (-1=ccw, 1=cw)
            relative,  # param4: 0 = absolute, 1 = relative
            0,  # param5: Meaningless
            0,  # param6: Meaningless
            0)  # param7: Meaningless
    finally:
        sem.release()
