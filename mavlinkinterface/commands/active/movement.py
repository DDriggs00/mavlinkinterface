from pymavlink import mavutil           # for everything
from math import pi, sin, cos           # for movement direction

from mavlinkinterface.logger import getLogger


def move3d(mcParams, sem, kill, throttleX, throttleY, throttleZ, time):
    '''Throttle functions are integers from -100 to 100'''
    try:
        log = getLogger("Movement")
        log.info("Moving in direction X=" + str(throttleX)
                 + " Y=" + str(throttleY)
                 + " Z=" + str(throttleZ)
                 + " for " + str(time) + " seconds")

        # Set the movement parameters
        mcParams['x'] = 10 * throttleX
        mcParams['y'] = 10 * throttleY
        mcParams['z'] = 5 * throttleZ + 500

        # Wait
        if kill.wait(timeout=time):
            # if killed
            log.trace("Function Move3d with x=" + str(throttleX)
                      + ", y=" + str(throttleX)
                      + ", z=" + str(throttleZ)
                      + ", t=" + str(time)
                      + " was prematurely halted")

    finally:
        # Return movement params to normal (but only those that were modified)
        mcParams['x'] = 0
        mcParams['y'] = 0
        mcParams['z'] = 500

        sem.release()
        log.trace('move3d ended')


def move(mcParams, sem, kill, direction, time, throttle=50):
    '''
    Modes the drone in 2 dimensions

    :param direction: The angle (from -180 to 180) at which to move the drone
    :param time: The number of seconds to thrust for
    :param throttle: The percentage of total thrust to use
    '''
    try:
        log = getLogger("Movement")
        log.info("Moving in direction: " + str(direction)
                 + " at " + str(throttle) + "% throttle"
                 + " for " + str(time) + " seconds")

        # Calculate x and y values
        x = cos(pi * direction / 180)
        y = sin(pi * direction / 180)
        scaler = (1000 / max(abs(x), abs(y))) * (throttle / 100)
        x = round(x * scaler)
        y = round(y * scaler)

        # Set movement parameters
        mcParams['x'] = x
        mcParams['y'] = y

        # wait
        if kill.wait(timeout=time):
            # If killed
            log.trace("Function Move with direction=" + str(direction)
                      + ", throttle=" + str(throttle)
                      + ", t=" + str(time)
                      + " was prematurely halted")

    finally:
        # Reset movement parameters
        mcParams['x'] = 0
        mcParams['y'] = 0

        sem.release()
        log.trace('move ended')


def diveTime(mcParams, sem, kill, time, throttle):
    '''
    :param time: the number of seconds to power the thrusters
    :param throttle: Throttle value is from -100 to 100, with negative indicating down
    '''
    try:
        log = getLogger("Movement")
        log.info("Diving at " + str(throttle) + "% throttle for " + str(time) + " seconds")

        # set movement parameters
        mcParams['z'] = (throttle * 5) + 500

        # wait
        if kill.wait(timeout=time):
            # if killed
            log.trace("Function diveTime with throttle=" + str(throttle)
                      + ", t=" + str(time)
                      + " was prematurely halted")

    finally:
        # reset movement parameters
        mcParams['z'] = 500

        sem.release()
        log.trace('diveTime ended')


def dive(mli, kill, depth, throttle=50, absolute=False):
    '''
    :param depth: The change in depth, negative being down
    :param throttle: Percent of thruster power to use
    '''
    try:
        if throttle > 75:
            acceptThreshold = .33
            safetyThreshold = .5
        elif throttle > 50:
            acceptThreshold = .15
            safetyThreshold = .33
        elif throttle > 25:
            acceptThreshold = .05
            safetyThreshold = .15
        else:
            acceptThreshold = 0
            safetyThreshold = .05

        log = getLogger("Movement")
        log.info("Diving to depth=" + str(depth)
                 + " at throttle=" + str(throttle)
                 + "% power, absolute=" + str(absolute))

        # set depth acceptance and safety thresholds
        if throttle > 75:
            acceptThreshold = .33
            safetyThreshold = .5
        elif throttle > 50:
            acceptThreshold = .15
            safetyThreshold = .33
        elif throttle > 25:
            acceptThreshold = .05
            safetyThreshold = .15
        else:
            acceptThreshold = 0
            safetyThreshold = .08

        # set target depth
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

        # set movement parameters
        if currentDepth > targetDepth + acceptThreshold:    # Need to descend
            descend = True
            mli.manualControlParams['z'] = 500 - (throttle * 5)
        elif currentDepth < targetDepth - acceptThreshold:  # Need to ascend
            descend = False
            mli.manualControlParams['z'] = 500 + (throttle * 5)
        else:
            log.trace('Already at desired depth')
            return

        i = 0
        oldDepth = currentDepth
        while not kill.wait(timeout=0.25):

            currentDepth = mli.getDepth()

            # if drone has descended or ascended far enough
            if descend and currentDepth < targetDepth + acceptThreshold:
                break
            if not descend and currentDepth > targetDepth - acceptThreshold:
                break

            if i == 12:     # every 3 seconds
                # if the drone has been thrusting for 3 seconds, but has not moved
                if abs(oldDepth - currentDepth) <= safetyThreshold:

                    log.trace("Function dive with depth=" + str(depth)
                              + ", throttle=" + str(throttle)
                              + ", absolute=" + str(absolute)
                              + " was prematurely halted due to a lack of movement")
                    break

                i = 0
                oldDepth = currentDepth

            i += 1

        if kill.is_set():
            log.trace("Function dive with depth=" + str(depth)
                      + ", throttle=" + str(throttle)
                      + ", absolute=" + str(absolute)
                      + " was prematurely halted")
    finally:
        # reset movement parameters
        mli.manualControlParams['z'] = 500

        mli.sem.release()
        log.trace('Dive function ended')


def surface(mli, kill):  # TODO
    log = getLogger("Movement")
    log.info("Rising to Surface")
    dive(mli, kill, 0, throttle=100, absolute=True)


def yawBeta(ml, sem, kill, angle, rate=20, direction=1, relative=1):
    try:
        log = getLogger("Movement")
        log.info("Yawing " + ("clockwise by " if (direction == 1) else "Counterclockwise by ")
                 + str(angle) + " degrees at " + str(rate) + " deg/s in "
                 + ("relative" if (relative == 1) else "Absolute") + " mode.")

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

        if kill.wait(timeout=((angle / rate) + .5)):     # Check if killEvent has been set
            log.trace("Function yawBeta with angle=" + str(angle)
                      + ", rate=" + str(rate)
                      + ", direction=" + str(direction)
                      + ", relative=" + str(relative)
                      + " was prematurely halted")
            return  # Stop executing function

    finally:
        sem.release()


def yawBasic(mcParams, sem, kill, angle, absolute=False):
    try:
        log = getLogger("Movement")
        log.info("Yawing by " + str(angle) + " degrees, absolute: " + str(absolute))

        mcParams['r'] = int(angle * (50 / 9))

        if kill.wait(timeout=(abs(int(angle * (50 / 9))) / 200)):   # Check if killEvent has been set
            log.trace("Function yaw with angle=" + str(angle)
                      + ", absolute=" + str(absolute)
                      + " was prematurely halted")

    finally:
        # reset movement parameters
        mcParams['r'] = 0

        sem.release()
        log.trace('yawTime ended')


def wait(ml, sem, kill, time):
    try:
        log = getLogger("Movement")
        log.warning("########## DEPRECATION WARNING ##########")
        log.warning("Wait function is deprecated, use sleep instead.")

        kill.wait(timeout=time)

    finally:
        sem.release()


def yaw(mli, kill, angle, absolute=False):   # TODO add rotational momentum to calculation
    '''
    Rotates the drone by *angle* degrees
    Note: This will never yaw by more than 180 degrees

    :param angle: The change in heading (in degrees), with negative being counterclockwise
    '''
    try:
        log = getLogger("Movement")
        log.info("Yawing by " + str(angle) + " absolute=" + str(absolute))

        currentHeading = mli.getHeading()
        if absolute:
            # In absolute mode, just face toward the input angle
            targetHeading = angle % 360
        else:   # relative
            # In relative mode, yaw by the input angle
            targetHeading = (angle + currentHeading) % 360

        log.trace('yaw: current: ' + str(currentHeading))
        log.trace('yaw: target: ' + str(targetHeading))

        if (targetHeading - currentHeading) % 360 <= 180:  # Clockwise

            mli.manualControlParams['r'] = 500
            while not kill.wait(timeout=.25):
                # Until within 30 degrees of target, yaw at 50%
                if (targetHeading - mli.getHeading()) % 360 <= 30:
                    break

            mli.manualControlParams['r'] = 250
            while not kill.wait(timeout=.25):
                # Until within 10 degrees of target, yaw at 25%
                if ((targetHeading - mli.getHeading()) % 360 <= 5
                        or (targetHeading - mli.getHeading()) % 360 > 330):
                    break

            mli.manualControlParams['r'] = -250
            while not kill.wait(timeout=.1):
                # Cancel momentum
                if mli.messages['ATTITUDE']['message'].yawspeed < 0.01:
                    break

        elif (targetHeading - currentHeading) % 360 > 180:  # Counterclockwise

            mli.manualControlParams['r'] = -500
            while not kill.wait(timeout=.25):
                # Until within 30 degrees of target, yaw at 50%
                if (targetHeading - mli.getHeading()) % 360 > 330:
                    break

            mli.manualControlParams['r'] = -250
            while not kill.wait(timeout=.25):
                # Until within 10 degrees of target, yaw at 25%
                if ((targetHeading - mli.getHeading()) % 360 > 355
                        or (targetHeading - mli.getHeading()) % 360 < 30):
                    break

            mli.manualControlParams['r'] = 250
            while not kill.wait(timeout=.1):
                # Cancel momentum
                if mli.messages['ATTITUDE']['message'].yawspeed > -0.01:
                    break

    finally:
        # reset yaw control to zero
        mli.manualControlParams['r'] = 0

        mli.sem.release()
        log.trace('yaw command ended')
