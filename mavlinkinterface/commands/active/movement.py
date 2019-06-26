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
                0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
                0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
            sleep(.25)
        ml.mav.manual_control_send(
            ml.target_system,
            0,  # x [back(-1000), forward(1000)]
            0,  # y [left(-1000), right(1000)]
            500,  # z [down(0), up(1000)]
            0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
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
                0,      # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
                0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
            sleep(.25)
        ml.mav.manual_control_send(
            ml.target_system,
            0,      # x [ forward(1000)-backward(-1000)]
            0,      # y [ left(-1000)-right(1000) ]
            500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
            0,      # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
            0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]

    finally:
        sem.release()

def diveTime(ml, sem, time, throttle):
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
                0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
                0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
            sleep(0.25)
        ml.mav.manual_control_send(
            ml.target_system,
            0,  # x [ forward(1000)-backward(-1000)]
            0,  # y [ left(-1000)-right(1000) ]
            500,  # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
            0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
            0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        sem.release()


def dive(mli, depth, throttle=100, absolute=False):
    '''
    :param depth: The change in depth, negative being down
    :param throttle: Percent of thruster power to use
    '''
    try:
        log = getLogger("Movement")
        log.info("Diving to depth=" + str(depth) + " at throttle=" + str(throttle) + "% power, absolute=" + str(absolute))
        currentDepth = mli.getDepth()

        if absolute:
            # In absolute mode, just go to a depth
            targetDepth = depth
        else:   # relative
            # In relative mode, go up/down by a depth
            targetDepth = depth + currentDepth

        if targetDepth > 0:
            log.error("Cannot Rise above the Surface, aborting")
            raise ValueError("Cannot Rise above the Surface, aborting command")
        i = 0
        oldDepth = currentDepth
        stuck = False
        # If the drone is below the desired depth
        if currentDepth > targetDepth:     # Need to Dive
            z = (throttle * 5) + 500 * -1
            while currentDepth > targetDepth + .5 and not stuck:     # Until within 1.5m of target, thrust at desired throttle
                currentDepth = mli.getDepth()
                mli.mavlinkConnection.mav.manual_control_send(
                    mli.mavlinkConnection.target_system,
                    0,  # x [ forward(1000)-backward(-1000)]
                    0,  # y [ left(-1000)-right(1000) ]
                    z,  # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
                    0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
                    0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
                if i == 12:                                 # If, over the course 3 sec
                    if -1 <= oldDepth - currentDepth <= 1:  # If depth has not changed
                        stuck = True                        # The drone must either be stuck or at the surface, but miscalibrated
                    i = 0
                    oldDepth = currentDepth
                i += 1
                sleep(.25)
        # If the drone is below the desired depth
        elif currentDepth < targetDepth:
            z = (throttle * 5) + 500
            while currentDepth < targetDepth + .5 and not stuck:     # Until within 1.5m of target, thrust at desired throttle
                currentDepth = mli.getDepth()
                mli.mavlinkConnection.mav.manual_control_send(
                    mli.mavlinkConnection.target_system,
                    0,  # x [ forward(1000)-backward(-1000)]
                    0,  # y [ left(-1000)-right(1000) ]
                    z,  # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
                    0,  # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
                    0)  # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
                if i == 12:                                 # If, over the course 3 sec
                    if -1 <= oldDepth - currentDepth <= 1:  # If depth has not changed
                        stuck = True                        # The drone must either be stuck or at the surface, but miscalibrated
                    i = 0
                    oldDepth = currentDepth
                i += 1
                sleep(.25)

        # Stop thrusting when the desired depth has been reached
        mli.mavlinkConnection.mav.manual_control_send(
            mli.mavlinkConnection.target_system,
            0,      # x [ forward(1000)-backward(-1000)]
            0,      # y [ left(-1000)-right(1000) ]
            500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
            0,      # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
            0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        mli.sem.release()

def surface(mli):  # TODO
    log = getLogger("Movement")
    log.info("Rising to Surface")
    dive(mli, 0, throttle=100, absolute=True)


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

def wait(ml, sem, time):
    try:
        log = getLogger("Movement")
        log.info("Waiting (with manual control set) for " + str(time) + " seconds")
        for i in range(0, time * 4):
            ml.mav.manual_control_send(
                ml.target_system,
                0,      # x [ forward(1000)-backward(-1000)]
                0,      # y [ left(-1000)-right(1000) ]
                500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle. ]
                0,      # r [ 500 will turn the drone 90 degrees ]
                0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1 ]
            sleep(.25)

    finally:
        sem.release()

def yaw2(mli, angle, absolute=False):   # TODO add rotational momentum to calculation
    '''
    Rotates the drone by *angle* degrees

    :param angle: The change in heading (in degrees), with negative being counterclockwise
    '''
    try:
        log = getLogger("Movement")
        log.info("Yawing by " + str(angle) + " absolute=" + str(absolute))
        currentHeading = mli.getHeading()
        log.debug(currentHeading)
        if absolute:
            # In absolute mode, just face toward the input angle
            targetHeading = angle
        else:   # relative
            # In relative mode, yaw by the input angle
            targetHeading = angle + currentHeading

        # If the drone must rotate
        if currentHeading > targetHeading:  # Counterclockwise
            i = 0
            while currentHeading > targetHeading + 2:     # Until within 2 degrees of target, yaw at 25%
                if not i % 10:
                    mli.mavlinkConnection.mav.manual_control_send(
                        mli.mavlinkConnection.target_system,
                        0,      # x [ forward(1000)-backward(-1000)]
                        0,      # y [ left(-1000)-right(1000) ]
                        500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
                        -250,   # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
                        0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
                sleep(.1)
                i += 1
                currentHeading = mli.getHeading()

        # If the drone must rotate clockwise
        if currentHeading < targetHeading:  # Clockwise
            i = 0
            while currentHeading < targetHeading - 2:     # Until within 2 degrees of target, yaw at 25%
                if not i % 10:
                    mli.mavlinkConnection.mav.manual_control_send(
                        mli.mavlinkConnection.target_system,
                        0,      # x [ forward(1000)-backward(-1000)]
                        0,      # y [ left(-1000)-right(1000) ]
                        500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
                        250,    # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
                        0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
                sleep(.1)
                i += 1
                currentHeading = mli.getHeading()

        while mli.messages['ATTITUDE'].yawspeed > 0.0012:
            mli.mavlinkConnection.mav.manual_control_send(
                mli.mavlinkConnection.target_system,
                0,      # x [ forward(1000)-backward(-1000)]
                0,      # y [ left(-1000)-right(1000) ]
                500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
                250,    # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
                0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
            sleep(.05)

        # Stop thrusting when the desired depth has been reached
        mli.mavlinkConnection.mav.manual_control_send(
            mli.mavlinkConnection.target_system,
            0,      # x [ forward(1000)-backward(-1000)]
            0,      # y [ left(-1000)-right(1000) ]
            500,    # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.]
            0,    # r [ corresponds to a twisting of the joystick, with counter-clockwise being negative. Corresponds to Yaw]
            0)      # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        mli.sem.release()
