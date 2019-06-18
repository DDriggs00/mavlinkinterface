from time import sleep                  # for everything
from pymavlink import mavutil           # for everything
from math import pi, sin, cos           # for movement direction

from mavlinkinterface.logger import getLogger

def move3d(ml, sem, throttleX, throttleY, throttleZ, time):
    '''Throttle functions are integers from -100 to 100'''
    try:
        log = getLogger("Movement")
        log.info("Moving in direction X=" + str(throttleX) + " Y=" + str(throttleY) + " Z=" + str(throttleZ) + " for " + str(time) + " seconds")
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
    :param time: The number of seconds to thrust for
    :param throttle: The percentage of total thrust to use
    '''
    try:
        log = getLogger("Movement")
        log.info("Moving in direction: " + str(direction) + " at " + str(throttle) + "% throttle for " + str(time) + " seconds")
        x = cos(pi * direction / 180)
        y = sin(pi * direction / 180)
        scaler = (1000 / max(abs(x), abs(y))) * (throttle / 100)
        x = round(x * scaler)
        y = round(y * scaler)

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

def dive(ml, sem, time, throttle):
    '''
    :param time: the number of seconds to power the thrusters
    :param throttle: Throttle value is from -100 to 100, with negative indicating down
    '''
    try:
        log = getLogger("Movement")
        log.info("Diving at " + str(throttle) + "% throttle for " + str(time) + " seconds")
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

def surface(ml, sem):  # TODO
    from mavlinkinterface.commands.active.beta_commands import diveDepth
    diveDepth(ml, sem, 0, throttle=100, absolute=True)


def yawBeta(ml, sem, angle, rate=20, direction=1, relative=0):
    try:
        log = getLogger("Movement")
        log.info("Yawing " + ("clockwise by " if (direction == 1) else "Counterclockwise by ") + str(angle) + " degrees at " + str(rate) + " deg/s in " + ("relative" if (relative == 1) else "Absolute") + " mode.")

        ml.mav.command_long_send(
            ml.target_system,
            ml.target_component,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,
            0,          # Confirmation
            angle,      # param 1: target angle (deg)
            rate,       # param 2: angular speed (deg/s)
            direction,  # param 3: direction (-1=ccw, 1=cw)
            relative,   # param 4: 0 = absolute, 1 = relative
            0,          # param 5: Empty
            0,          # param 6: Empty
            0)          # param 7: Empty

        sleep((angle / rate) + .5)
    finally:
        sem.release()

def yaw(ml, sem, angle, absolute=False):
    try:
        log = getLogger("Movement")
        log.info("Yawing by " + str(angle) + " degrees")
        r = int(angle * (50 / 9))
        ml.mav.manual_control_send(
            ml.target_system,
            0,      # x [ forward(1000)-backward(-1000)]
            0,      # y [ left(-1000)-right(1000) ]
            500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle. ]
            r,      # r [ 500 will turn the drone 90 degrees ]
            0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1 ]
        sleep(abs(r) / 200)

    finally:
        sem.release()
