# Regular Imports
from pymavlink import mavutil           # For pretty much everything
from threading import Thread            # For pretty much everything
from threading import Semaphore         # To prevent multiple movement commands at once
# from queue import Queue                 # For queuing mode
import logging                          # For logging
# import platform                         # For choosing log location
from configparser import ConfigParser   # For configuration details

# Local Imports
from mavlinkinterface.logger import get_logger              # For Logging
import mavlinkinterface.commands as commands                # For calling commands
from mavlinkinterface.rthread import RThread                # For functions that have return values
from mavlinkinterface.datarefresher import dataRefresher    # For keeping the message socket clean
from mavlinkinterface.enum.queueModes import queueModes     # For use in async mode

class mavlinkInterface(object):
    '''
    This is the main interface to Mavlink. All calls will be made through this object.
    '''
    # Internal Commands
    def __init__(self, queueMode=queueModes.override, asynchronous=False):
        '''
        Creates a new mavlinkInterface Object
        :param queueMode: See docs/configuration/setDefaultQueueMode for details.\n
        :param asynchronous: When false or not given, movement commands will return once the movement is done.  When true, movement commands will return immediately and execute in the background.
        '''

        get_logger("Main")

        # Import config values
        logging.debug("importing configuration file")
        self.config = ConfigParser()
        self.config.read("mavlinkinterface/config.cfg")

        # Set class variables
        logging.debug("Setting class variables")
        self.queueMode = queueMode
        self.asynchronous = asynchronous
        self.lightBrightness = 0

        # Create Semaphore
        self.sem = Semaphore(1)

        # Set up Mavlink
        logging.info("Initializing MavLink Connection")
        connectionString = 'udp:' + self.config['mavlink']['connection_ip'] + ':' + self.config['mavlink']['connection_port']
        self.mavlinkConnection = mavutil.mavlink_connection(connectionString)
        self.mavlinkConnection.wait_heartbeat()
        logging.info("Successfully connected to target.")
        print("Successfully connected to target.")

        # start dataRefresher
        self.refresher = Thread(target=dataRefresher, args=(self.mavlinkConnection,))
        logging.info("Started dataRefresher process")

    def __del__(self):
        '''Clean up while exiting
        Note: No logging may happen here due to a bug when using exit() that I can't figure out
        '''
        # Stop dataRefresher process
        self.refresher.kill()
        # Disarm
        self.__getSemaphore(override=True)
        commands.active.disarm(self.mavlinkConnection, self.sem)

    # Private functions
    def __getSemaphore(self, override):     # contains TODO
        '''Attempts to acquire the movement semaphore based on queuemode. Returns true if semaphore was acquired, false otherwise.'''
        if not self.sem.acquire(blocking=False):    # Semaphore could not be acquired, proceeding by mode
            if self.queueMode == queueModes.override or override:
                print("Override active, Killing existing task")
                logging.info("Override active, Killing existing task")
                if self.queueMode == queueModes.queue:
                    # TODO Empty queue
                    pass
                self.stopCurrentTask()  # Will release semaphore
                self.sem.acquire()
                return True     # Now that previous action has been killed, execute current action
            elif self.queueMode == queueModes.ignore:
                print("Using Ignore mode, this command will now be discarded")
                logging.info("Using Ignore mode, command ignored")
                return False    # The command should not be executed
            elif self.queueMode == queueModes.queue:
                print("Using queue Mode, Adding item to queue")
                logging.info("Using queue Mode, Adding item to queue")
                print("This mode does nothing currently. The command will be ignored")  # TODO
                return False    # The command needs not be executed
        return True     # If the semaphore was obtained on the first try

    # General commands
    def help(self):     # TODO
        print("Available functions:")
        print("move(direction, ):")
        print("stopCurrentTask():")
        print("setLights(brightness)")
        print("setFlightMode(mode)")

    def stopAll(self):  # contains TODO
        if self.queueMode == queueModes.queue:
            # TODO Clear queue
            pass
        self.stopCurrentTask()

    def stopCurrentTask(self):  # TODO
        # Kills the currently running task and stops the submarine
        pass

    # Active commands
    def arm(self, override=False):
        '''Enables the thrusters'''
        if not self.__getSemaphore(override):
            return

        logging.info("Arming")
        self.t = Thread(target=commands.active.arm, args=(self.mavlinkConnection, self.sem,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def disarm(self, override=False):
        '''Disables the thrusters'''
        if not self.__getSemaphore(override):
            return

        logging.info("Disarming")
        self.t = Thread(target=commands.active.disarm, args=(self.mavlinkConnection, self.sem,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def dive(self, time, throttle, override=False):
        '''
        Thrust vertically for a specified amount of time

        :param time: how long to thrust in seconds
        :param throttle: percent throttle to use, -100 = full down, 100 = full up
        '''
        if not self.__getSemaphore(override):
            return

        logging.info("Diving at " + str(throttle) + "% throttle for " + str(time) + " seconds")
        self.t = Thread(target=commands.active.dive, args=(self.mavlinkConnection, self.sem, time, throttle,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def diveDepth(self, depth, throttle=100, absolute=False, override=False):
        '''
        Move vertically by a certain distance, or to a specific altitude

        :param depth: Distance to dive or rise. Deeper is negative
        :param throttle: Percent throttle to use
        :param absolute <optional>: When True, dives to the depth given relative to sea level
        '''
        if not self.__getSemaphore(override):
            return

        self.t = Thread(target=commands.active.diveDepth, args=(self.mavlinkConnection, self.sem, depth, throttle, absolute,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def gripperOpen(self, override=False):
        '''
        Opens the Gripper Arm
        '''
        if not self.__getSemaphore(override):
            return

        self.t = Thread(target=commands.active.gripperOpen, args=(self.mavlinkConnection, self.sem,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def gripperClose(self, override=False):
        '''
        Closes the Gripper Arm
        '''
        if not self.__getSemaphore(override):
            return

        self.t = Thread(target=commands.active.gripperClose, args=(self.mavlinkConnection, self.sem,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def yaw(self, angle, override=False):
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees
        '''
        if not self.__getSemaphore(override):
            return

        logging.info("Yawing " + str(angle) + " degrees")
        self.t = Thread(target=commands.active.yaw, args=(self.mavlinkConnection, self.sem, angle,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def move(self, direction, time, throttle=100, absolute=False, override=False):
        '''
        Move horizontally in any direction

        Parameter Direction: the angle (in degrees) to move toward
        Parameter time: the time (in seconds) to power the thrusters
        Parameter throttle: the percentage of thruster power to use
        Parameter Absolute: When true, an angle of 0 degrees is magnetic north
        '''
        if not self.__getSemaphore(override):
            return

        logging.info("Moving in direction: " + str(direction) + " at " + str(throttle) + "% throttle for " + str(time) + "seconds")
        self.t = Thread(target=commands.active.move, args=(self.mavlinkConnection, self.sem, direction, time, throttle,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def move3d(self, throttleX, throttleY, throttleZ, time, override=False):
        '''
        Move in any direction

        Parameter Throttle X: Percent power to use when thrusting in the X direction
        Parameter Throttle Y: Percent power to use when thrusting in the Y direction
        Parameter Throttle Z: Percent power to use when thrusting in the Z direction
        Parameter Time: The time (in seconds) to power the thrusters
        '''
        if not self.__getSemaphore(override):
            return

        logging.info("Moving in direction x=" + str(throttleX) + " y=" + str(throttleY) + " z=" + str(throttleZ) + " for " + str(time) + "seconds")
        self.t = Thread(target=commands.active.move3d, args=(self.mavlinkConnection, self.sem, throttleX, throttleY, throttleZ, time,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def setFlightMode(self, mode, override=False):
        '''
        Sets the flight mode of the drone.
        Valid modes are listed in docs/active/setFlightMode.md

        Parameter Mode: The mode to use
        '''
        if not self.__getSemaphore(override):
            return

        logging.info("Setting flight mode to " + str(mode))
        self.t = Thread(target=commands.active.setFlightMode, args=(self.mavlinkConnection, self.sem, mode,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    # def setLights(self, brightness, override=False):     # Broken
    #     '''Sets the lights to the specified brightness(rounded to the nearest brightness level)

    #     Parameter brightness: The percentage brightness to use for the lights
    #     '''
    #     if not self.__getSemaphore(override):
    #         return

    #     # self.lightBrightness = brightness
    #     self.t = Thread(target=commands.active.lightsMax, args=(self.mavlinkConnection, self.sem,))
    #     self.t.start()
    #     if(not self.asynchronous):
    #         self.t.join()

    # Sensor reading commands
    def getBatteryData(self):
        '''Returns a JSON containing battery Data'''
        logging.info("Fetching battery Data JSON")
        self.t = RThread(target=commands.passive.getBatteryData, args=(self.mavlinkConnection,))
        self.t.start()
        return self.t.join()

    def getAccelerometerData(self):
        '''Returns a JSON containing Accelerometer Data'''
        logging.info("Fetching Accelerometer Data JSON")
        self.t = RThread(target=commands.passive.getAccelerometerData, args=(self.mavlinkConnection,))
        self.t.start()
        return self.t.join()

    def getGyroscopeData(self):
        '''Returns a JSON containing Gyroscope Data'''
        logging.info("Fetching Gyroscope Data JSON")
        self.t = RThread(target=commands.passive.getGyroscopeData, args=(self.mavlinkConnection,))
        self.t.start()
        return self.t.join()

    def getMagnetometerData(self):
        '''Returns a JSON containing Magnetometer Data'''
        logging.info("Fetching Magnetometer Data JSON")
        self.t = RThread(target=commands.passive.getMagnetometerData, args=(self.mavlinkConnection,))
        self.t.start()
        return self.t.join()

    def getIMUData(self):
        '''Returns a JSON containing IMU Data'''
        logging.info("Fetching IMU Data JSON")
        self.t = RThread(target=commands.passive.getIMUData, args=(self.mavlinkConnection,))
        self.t.start()
        return self.t.join()

    def getPressureExternal(self):
        '''Returns the external pressure as a float'''
        logging.info("Fetching External Pressure")
        self.t = RThread(target=commands.passive.getPressureExternal, args=(self.mavlinkConnection,))
        self.t.start()
        return self.t.join()

    def getDepth(self):
        '''Returns the depth of the drone as a float'''
        logging.info("Fetching Depth")
        self.t = RThread(target=commands.passive.getDepth, args=(self.mavlinkConnection,))
        self.t.start()
        return self.t.join()

    # Beta Commands
    def yawBeta(self, angle, rate=20, direction=1, relative=1, override=False):     # Broken
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees

        rate: rotational velocity in deg/s

        direction: 1 = Clockwise, -1 = CCW

        relative: (1) - zero is current bearing, (0) - zero is north
        '''
        if not self.__getSemaphore(override):
            return

        logging.info("Yawing " + ("clockwise by " if (direction == 1) else "Counterclockwise by ") + str(angle) + " degrees at " + str(rate) + " deg/s in " + ("relative" if (relative == 1) else "Absolute") + " mode.")
        self.t = Thread(target=commands.active.yawBeta, args=(self.mavlinkConnection, self.sem, angle, rate, direction, relative,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()

    def changeAltitude(self, rate, altitude, override=False):
        if not self.__getSemaphore(override):
            return

        logging.info("Moving to altitude " + str(altitude) + " at " + str(rate) + " m/s.")
        self.t = Thread(target=commands.active.changeAltitude, args=(self.mavlinkConnection, self.sem, rate, altitude,))
        self.t.start()
        if(not self.asynchronous):
            self.t.join()
