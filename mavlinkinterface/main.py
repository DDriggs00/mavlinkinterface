# Regular Imports
from pymavlink import mavutil           # For pretty much everything
from threading import Thread            # For pretty much everything
from threading import Semaphore         # For keeping only one thread running
# from queue import Queue                 # For queuing mode
from datetime import datetime           # For naming log file
import logging                          # For logging
from configparser import ConfigParser   # For configuration details

# Local Imports
import mavlinkinterface.commands as commands
from mavlinkinterface.enum.queueModes import queueModes
from mavlinkinterface.enum.flightModes import flightModes

class mavlinkInterface(object):
    '''
    This is the main interface to Mavlink
    '''
    def __init__(self, queueMode=queueModes.override, asynchronous=False):
        '''
        Creates a new mavlinkInterface Object
        @param queueMode See docs/configuration/setDefaultQueueMode for details.\n
        @param asynchronous When false or not given, movement commands will return once the movement is done.  When true, movement commands will return immediately and execute in the background.
        '''
        # Set up Logging
        logFileName = ('log_' + str(datetime.now()) + '.log').replace(':', '.')
        logging.basicConfig(filename=logFileName,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
        # Import config values
        logging.debug("importing configuration file")
        self.config = ConfigParser()
        self.config.read("mavlinkinterface/config.cfg")
        # Set class variables
        logging.debug("Setting class variables")
        self.queueMode = queueMode
        self.asynchronous = asynchronous
        self.lightBrightness = 0
        self.flightMode = flightModes.manual
        # Create Semaphore
        self.sem = Semaphore(1)
        # Set up Mavlink
        logging.info("Initializing MavLink Connection")
        connectionString = 'udp:' + self.config['mavlink']['connection_ip'] + ':' + self.config['mavlink']['connection_port']
        self.mavlinkConnection = mavutil.mavlink_connection(connectionString)
        self.mavlinkConnection.wait_heartbeat()
        logging.info("Successfully connected to target.")
        print("Successfully connected to target.")

    def __del__(self):
        self.disarm()
        pass

    def __getSemaphore(self, override):
        '''Attempts to acquire the movement semaphore based on queuemode. Returns true if semaphore was acquired, false otherwise.'''
        if not self.sem.acquire(blocking=False):  # Semaphore could not be acquired, proceeding by mode
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
                return False    # The command needs not be executed
            elif self.queueMode == queueModes.queue:
                print("Using queue Mode, Adding item to queue")
                logging.info("Using queue Mode, Adding item to queue")
                print("This mode does nothing atm. The command will be ignored")  # TODO
                return False    # The command needs not be executed
        return True

    def help(self):     # TODO
        print("Available functions:")
        print("move(direction, ):")
        print("stopCurrentTask():")
        print("setLights(brightness)")
        print("setFlightMode(mode)")

    def stopAll(self):  # TODO finish
        if self.queueMode == queueModes.queue:
            # Clear queue
            pass
        self.stopCurrentTask()

    def stopCurrentTask(self):  # TODO
        # Kills the currently running task and stops the submarine
        pass

    def setLightsMax(self, override=False):
        if not self.__getSemaphore(override):
            return

        # self.lightBrightness = brightness
        t = Thread(target=commands.active.lightsMax, args=(self.mavlinkConnection, self.sem,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def setLightsOff(self, override=False):
        if not self.__getSemaphore(override):
            return

        # self.lightBrightness = brightness
        t = Thread(target=commands.active.lightsoff, args=(self.mavlinkConnection, self.sem,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def dive(self, time, throttle, override=False):
        if not self.__getSemaphore(override):
            return

        logging.info("Diving at " + str(throttle) + "% throttle for " + str(time) + " seconds")
        t = Thread(target=commands.active.dive, args=(self.mavlinkConnection, self.sem, time, throttle,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def yaw(self, angle, override=False):
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees
        '''
        if not self.__getSemaphore(override):
            return

        logging.info("Yawing " + str(angle) + " degrees")
        t = Thread(target=commands.active.yaw, args=(self.mavlinkConnection, self.sem, angle,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def yawBeta(self, angle, rate=20, direction=1, relative=1, override=False):
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees

        rate: rotational velocity in deg/s

        direction: 1 = Clockwise, -1 = CCW

        relative: (1) - zero is current bearing, (0) - zero is north
        '''
        if not self.__getSemaphore(override):
            return

        logging.info("Yawing " + ("clockwise by " if (direction == 1) else "Counterclockwise by ") + str(angle) + " degrees at " + str(rate) + " deg/s in " + ("relative" if (relative == 1) else "Absolute") + " mode.")
        t = Thread(target=commands.active.yawBeta, args=(self.mavlinkConnection, self.sem, angle, rate, direction, relative,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def changeAltitude(self, rate, altitude, override=False):
        if not self.__getSemaphore(override):
            return

        logging.info("Moving to altitude " + str(altitude) + " at " + str(rate) + " m/s.")
        t = Thread(target=commands.active.changeAltitude, args=(self.mavlinkConnection, self.sem, rate, altitude,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def move(self, direction, time, throttle=100, override=False):
        if not self.__getSemaphore(override):
            return

        logging.info("Moving in direction: " + str(direction) + " at " + str(throttle) + "% throttle for " + str(time) + "seconds")
        t = Thread(target=commands.active.move, args=(self.mavlinkConnection, self.sem, direction, time, throttle,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def move3d(self, throttleX, throttleY, throttleZ, time, override=False):
        if not self.__getSemaphore(override):
            return

        logging.info("Moving in direction x=" + str(throttleX) + " y=" + str(throttleY) + " z=" + str(throttleZ) + " for " + str(time) + "seconds")
        t = Thread(target=commands.active.move3d, args=(self.mavlinkConnection, self.sem, throttleX, throttleY, throttleZ, time,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def setFlightMode(self, mode, override=False):
        if not self.__getSemaphore(override):
            return

        logging.info("Setting flight mode to " + str(mode))
        self.flightMode = mode
        t = Thread(target=commands.active.setFlightMode, args=(self.mavlinkConnection, self.sem, mode,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def getFlightMode(self):
        return self.flightMode

    def arm(self, override=False):
        if not self.__getSemaphore(override):
            return

        logging.info("Arming")
        t = Thread(target=commands.active.arm, args=(self.mavlinkConnection, self.sem,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def disarm(self, override=False):
        if not self.__getSemaphore(override):
            return

        logging.info("Disarming")
        t = Thread(target=commands.active.disarm, args=(self.mavlinkConnection, self.sem,))
        t.start()
        if(not self.asynchronous):
            t.join()


# class queueManager(Queue):
#     def __init__(self, maxsize):
#         return super().__init__(maxsize)

class RThread(Thread):    # https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        try:
            if self._target is not None:
                self._return = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
