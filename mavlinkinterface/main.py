# Regular Imports
from pymavlink import mavutil           # For pretty much everything
from threading import Thread            # For pretty much everything
from threading import Event             # For killing threads
from threading import Semaphore         # To prevent multiple movement commands at once
from queue import Queue, Empty          # For queuing mode
import json                             # For returning JSON-formatted strings
from time import sleep                  # For waiting for heartbeat message validation
from datetime import datetime           # For Initial log comment
from configparser import ConfigParser   # For config file management
from os.path import abspath             # For config file management
from os.path import expanduser          # for config file management
from os.path import exists              # For checking if config file exists
from pymavlink.mavextra import mag_heading  # Pre-Built function to calculate heading

# Local Imports
from mavlinkinterface.logger import getLogger               # For Logging
import mavlinkinterface.commands as commands                # For calling commands
# from mavlinkinterface.rthread import RThread                # For functions that have return values
# from mavlinkinterface.enum.execModes import execModes     # For use in async mode


class mavlinkInterface(object):
    '''
    This is the main interface to Mavlink. All calls will be made through this object.
    '''

    # Internal Commands
    def __init__(self, execMode):
        '''
        Creates a new mavlinkInterface Object

        :param execMode: The Execution mode to use when not given as a parameter.
                         See docs/configuration/setDefaultexecMode for details.\n
        '''
        if execMode not in ['synchronous', 'queue', 'ignore', 'override']:
            raise ValueError('The execMode parameter must be one of the following:\n'
                             + ' synchronous, queue, ignore, override')

        # Initialize logger
        self.log = getLogger('Main', doPrint=True)
        self.log.debug('################################################################################')
        self.log.debug('###################### New Log ' + str(datetime.now()) + ' ######################')
        self.log.debug('################################################################################')

        # Import config values
        self.config = ConfigParser()
        self.configPath = abspath(expanduser('~/.mavlinkInterface.ini'))
        if exists(self.configPath):
            self.log.debug('importing configuration file from path: ' + self.configPath)
            self.config.read(self.configPath)
        else:   # Config file does not exist
            # Populate file with Default config options
            self.config['mavlink'] = {'connection_ip': '0.0.0.0',
                                      'connection_port': '14550'}
            self.config['geodata'] = {'COMMENT_1': 'The pressure in pascals at the surface of the body of water.',
                                      'COMMENT_1B': 'Sea Level is around 101325. Varies day by day',
                                      'surfacePressure': '101325',
                                      'COMMENT_2': 'The density of the diving medium. Pure water is 1000',
                                      'fluidDensity': '1000'}
            self.config['messages'] = {'pressureSensorExternal': 'SCALED_PRESSURE2'}
            self.config['hardware'] = {'sonarcount': '1'}
            # Save file
            self.config.write((open(self.configPath, 'w')))

        # Set class variables
        self.log.debug('Setting class variables')
        self.execMode = execMode

        # Create variables to contain mavlink message data
        self.messages = {}

        # Create Semaphore and Queue
        self.sem = Semaphore(1)
        self.q = Queue()

        # Set up Mavlink
        self.log.debug('Initializing MavLink Connection')
        connectionString = ('udp:' +
                            self.config['mavlink']['connection_ip'] +
                            ':' +
                            self.config['mavlink']['connection_port'])
        self.mavlinkConnection = mavutil.mavlink_connection(connectionString)
        self.mavlinkConnection.wait_heartbeat()                 # Start Heartbeat
        self.mavlinkConnection.mav.request_data_stream_send(    # Request start of message stream
            self.mavlinkConnection.target_system,
            self.mavlinkConnection.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_ALL,
            0x5,
            1)

        # Building Kill Events
        self.killEvent = Event()    # When set, will signal all attached tasks to stop
        self.currentTaskKillEvent = Event()     # When set, will kill the current task

        # start dataRefreshers
        self.refresher = Thread(target=self.__updateMessage, args=(self.killEvent,))
        self.refresher.daemon = True    # Kill on program end
        self.refresher.start()

        # start heartbeat maintainer
        self.heartbeatThread = Thread(target=self.__heartbeatMaintain, args=(self.killEvent,))
        self.heartbeatThread.daemon = True  # Kill on program end
        self.heartbeatThread.start()

        # start leak detection
        self.leakDetectorThread = Thread(target=self.__leakDetector, args=(self.killEvent,))
        self.leakDetectorThread.daemon = True   # Kill on program end
        self.leakDetectorThread.start()

        # Start Queue maintenance process
        self.queueThread = Thread(target=self.__queueManager, args=(self.killEvent,))
        self.queueThread.daemon = True   # Kill on program end
        self.queueThread.start()

        # Initiate light class
        self.lights = commands.active.lights()

        # Initiate sonar class
        if self.config['hardware']['sonarcount'] > 0:
            self.sonar = commands.passive.sonar()

        # Validating heartbeat
        self.log.info('Waiting for heartbeat')
        while 'HEARTBEAT' not in self.messages:
            sleep(.1)
        self.log.info('Successfully connected to target.')
        self.log.debug('__init__ end')

    def __del__(self):
        '''Clean up while exiting'''
        # NOTE: logging does not work in __del__ for some reason

        # Stop statusMonitor and DataRefresher processes
        try:
            # Stop child threads
            self.killEvent.set()

            # Disarm
            self.__getSemaphore(override=True)
            commands.active.disarm(self.mavlinkConnection, self.sem)
        except NameError:
            pass    # Initializer not finished

    # Private functions
    def __getSemaphore(self, mode, target):
        '''
        Attempts to acquire the movement semaphore based on execMode.
        Returns true if semaphore was acquired, false otherwise.
        '''

        if mode is None:
            mode = self.execMode

        if not self.sem.acquire(blocking=False):    # Semaphore could not be acquired, proceeding by mode

            if mode == 'synchronous':
                self.log.info('QueueMode = synchronous, waiting for queue and semaphore')
                try:
                    while self.q.qsize() > 0:
                        sleep(.1)
                    self.sem.acquire(blocking=True)
                except KeyboardInterrupt:
                    self.log.error('Keyboard interrupt received, aborting command')
                    return False

                return True

            if mode == 'override':
                self.log.info('Override active, Killing existing task(s)')
                self.stopAllTasks()
                if not self.sem.acquire(blocking=False):    # If the current task did not properly release the semaphore
                    self.sem.release()                      # Release it
                    self.sem.acquire()                      # Then re-take it
                return True     # Now that previous action has been killed, execute current action
            elif self.execMode == 'ignore':
                self.log.info('Using Ignore mode, command ignored')
                return False    # The command should not be executed

            elif self.execMode == 'queue':
                self.log.info('Using queue Mode, Adding item to queue')
                self.q.put(target)
                return False    # The command will be executed by the QueueManager process
        return True     # If the semaphore was obtained on the first try

    def __updateMessage(self, killEvent):
        '''This function automatically updates a variable to contain the contents of a mavlink message'''
        log = getLogger('Refresh')  # Log that this was started
        log.debug('dataRefresher Class Initiating.')
        logMessages = ['SYS_STATUS',
                       'RAW_IMU',
                       self.config['messages']['pressureSensorExternal'],
                       'HEARTBEAT',
                       'ATTITUDE',
                       'STATUSTEXT']
        while not killEvent.is_set():   # When killEvent is set, stop looping
            msg = None
            # try:
            msg = self.mavlinkConnection.recv_match(type=logMessages, blocking=True, timeout=1)
            # except:
            #     self.log.exception('')
            #     # TODO figure out which exception is periodically showing up
            # Timeout used so it has the chance to notice the stop flag when no data is present
            if msg:
                self.messages[str(msg.get_type())] = {'message': msg, 'time': datetime.now()}

    def __leakDetector(self, killEvent):
        '''This function continuously checks for leaks, and upon detecting a leak, runs the desired action'''
        log = getLogger('Status', doPrint=True)
        log.debug('Leak Detector started')
        while not killEvent.wait(timeout=1):
            if 'STATUSTEXT' in self.messages and 'LEAK' in str(self.messages['STATUSTEXT']['message']).upper():
                log.error('Leak Detected: ' + self.messages['STATUSTEXT']['message'])    # Write the message to the log
                self.dive(0, absolute=True)   # Then run the appropriate response

        log.debug('StatusMonitor Stopping')

    def __heartbeatSend(self, type=6, autopilot=8, base_mode=192, custom_mode=0, system_status=4, mavlink_version=3):
        '''
        The heartbeat message shows that a system is present and responding.
        The type of the MAV and Autopilot hardware allow the
        receiving system to treat further messages from this
        system appropriate (e.g. by laying out the user
        interface based on the autopilot).
        https://mavlink.io/en/messages/common.html#HEARTBEAT

        type                : Type of the MAV (quadrotor, helicopter, etc.) (type:uint8_t, values:MAV_TYPE)
        autopilot           : Autopilot type / class. (type:uint8_t, values:MAV_AUTOPILOT)
        base_mode           : System mode bitmap. (type:uint8_t, values:MAV_MODE_FLAG)
        custom_mode         : A bitfield for use for autopilot-specific flags (type:uint32_t)
        system_status       : System status flag. (type:uint8_t, values:MAV_STATE)
        mavlink_version     : MAVLink version, not writable by user.
                              Gets added by protocol because of magic data type: uint8_t_mavlink_version (type:uint8_t)

        According to https://discuss.bluerobotics.com/t/1515/2,
        "The values of these heartbeat fields is not really important here, I just used the same numbers that QGC uses"
        '''
        self.mavlinkConnection.mav.heartbeat_send(
            type,               # type
            autopilot,          # autopilot
            base_mode,          # base_mode
            custom_mode,        # custom_mode
            system_status,      # system_status
            mavlink_version)    # mavlink_version

    def __heartbeatMaintain(self, killEvent):
        self.log.debug('Heartbeat broadcast started')
        while not killEvent.wait(timeout=1):
            self.__heartbeatSend()
        self.log.debug('Heartbeat broadcast stopped')

    def __queueManager(self, killEvent):
        self.log.debug('queueManager starting')
        while not killEvent.wait(timeout=1):
            if self.q.qsize() > 0:
                if self.sem.acquire(blocking=True, timeout=1):
                    try:
                        t = self.q.get(block=False)
                        t.start()
                        t.join()
                    except Empty:
                        self.sem.release()

    # General commands
    def help(self):     # TODO
        print('Available functions:')
        print('move(direction, ):')
        print('stopCurrentTask():')
        print('setLights(brightness)')
        print('setFlightMode(mode)')

    def stopAllTasks(self):
        # Clear Queue
        while self.q.qsize() > 0:
            self.q.get(block=False)
        self.stopCurrentTask()

    def stopCurrentTask(self):
        # Kills the currently running task and stops the drone
        self.currentTaskKillEvent.set()

    # Active commands
    def arm(self, execMode=None):
        '''Enables the thrusters'''

        # Create thread object
        t = Thread(target=commands.active.arm, args=(self.mavlinkConnection, self.sem))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):    # If sem was able to be acquired
            t.start()                     # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def disarm(self, execMode=None):
        '''Disables the thrusters'''

        t = Thread(target=commands.active.disarm, args=(self.mavlinkConnection, self.sem,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):    # If sem was able to be acquired
            t.start()                     # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def setFlightMode(self, flightMode, execMode=None):
        '''
        Sets the flight mode of the drone.
        Valid modes are listed in docs/active/setFlightMode.md

        Parameter Mode: The mode to use
        '''
        t = Thread(target=commands.active.setFlightMode, args=(self.mavlinkConnection, self.sem, flightMode,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def move(self, direction, time, throttle=50, absolute=False, execMode=None):
        '''
        Move horizontally in any direction

        Parameter Direction: the angle (in degrees) to move toward
        Parameter time: the time (in seconds) to power the thrusters
        Parameter throttle: the percentage of thruster power to use
        Parameter Absolute: When true, an angle of 0 degrees is magnetic north
        '''
        t = Thread(target=commands.active.move,
                   args=(self.mavlinkConnection, self.sem, self.currentTaskKillEvent, direction, time, throttle,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def move3d(self, throttleX, throttleY, throttleZ, time, execMode=None):
        '''
        Move in any direction

        Parameter Throttle X: Percent power to use when thrusting in the X direction
        Parameter Throttle Y: Percent power to use when thrusting in the Y direction
        Parameter Throttle Z: Percent power to use when thrusting in the Z direction
        Parameter Time: The time (in seconds) to power the thrusters
        '''
        t = Thread(target=commands.active.move3d,
                   args=(self.mavlinkConnection, self.sem, self.currentTaskKillEvent,
                         throttleX, throttleY, throttleZ, time,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def dive(self, depth, throttle=50, absolute=False, execMode=None):
        '''
        Move vertically by a certain distance, or to a specific altitude

        :param depth: Distance to dive or rise. Deeper is negative
        :param throttle: Percent throttle to use
        :param absolute <optional>: When True, dives to the depth given relative to sea level
        '''
        t = Thread(target=commands.active.dive, args=(self, self.currentTaskKillEvent, depth, throttle, absolute,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def diveTime(self, time, throttle, execMode=None):
        '''
        Thrust vertically for a specified amount of time

        :param time: how long to thrust in seconds
        :param throttle: percent throttle to use, -100 = full down, 100 = full up
        '''
        t = Thread(target=commands.active.diveTime,
                   args=(self.mavlinkConnection, self.sem, self.currentTaskKillEvent, time, throttle,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def surface(self, execMode=None):
        '''
        Thrust upward at full power until reaching the surface
        '''
        t = Thread(target=commands.active.surface, args=(self, self.currentTaskKillEvent,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def yaw(self, angle, execMode=None):
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees
        '''
        t = Thread(target=commands.active.yaw,
                   args=(self.mavlinkConnection, self.sem, self.currentTaskKillEvent, angle,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def yaw2(self, angle, absolute=False, execMode=None):
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees
        '''
        t = Thread(target=commands.active.yaw2, args=(self, self.currentTaskKillEvent, angle, absolute,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def gripperOpen(self, execMode=None):
        '''
        Opens the Gripper Arm
        '''
        t = Thread(target=commands.active.gripperOpen, args=(self.mavlinkConnection, self.sem,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def gripperClose(self, execMode=None):
        '''
        Closes the Gripper Arm
        '''
        t = Thread(target=commands.active.gripperClose, args=(self.mavlinkConnection, self.sem,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    # Sensor reading commands
    def getBatteryData(self):
        '''Returns a JSON-formatted string containing battery data'''
        self.log.debug('Fetching battery data')

        # Check message availability
        if 'SYS_STATUS' not in self.messages:
            self.log.warn('SYS_STATUS message not available, waiting 1 sec')
            sleep(1)

        data = {}
        data['voltage'] = self.messages['SYS_STATUS']['message'].voltage_battery / 1000        # convert to volts
        data['current'] = self.messages['SYS_STATUS']['message'].current_battery
        data['percent_remaining'] = self.messages['SYS_STATUS']['message'].battery_remaining
        return json.dumps(data)

    def getAccelerometerData(self):
        '''Returns a JSON containing Accelerometer Data'''
        self.log.debug('Fetching Accelerometer Data')

        # Checking message availability
        if 'RAW_IMU' not in self.messages:
            self.log.warn('RAW_IMU message not available, waiting 1 sec')
            sleep(1)

        data = {}
        data['X'] = self.messages['RAW_IMU']['message'].xacc
        data['Y'] = self.messages['RAW_IMU']['message'].yacc
        data['Z'] = self.messages['RAW_IMU']['message'].zacc
        return json.dumps(data)

    def getGyroscopeData(self):
        '''Returns a JSON containing Gyroscope Data'''
        self.log.debug('Fetching Gyro Data')

        # Checking message availability
        if not self.messages.__contains__('RAW_IMU'):
            self.log.warn('RAW_IMU message not available, waiting 1 sec')
            sleep(1)

        data = {}
        data['X'] = self.messages['RAW_IMU']['message'].xgyro
        data['Y'] = self.messages['RAW_IMU']['message'].ygyro
        data['Z'] = self.messages['RAW_IMU']['message'].zgyro
        return json.dumps(data)

    def getMagnetometerData(self):
        '''Returns a JSON containing Magnetometer Data'''
        self.log.debug('Fetching magnetometer Data')
        if not self.messages.__contains__('RAW_IMU'):
            self.log.warn('RAW_IMU message not available, waiting 1 sec')
            sleep(1)

        data = {}
        data['X'] = self.messages['RAW_IMU']['message'].xmag
        data['Y'] = self.messages['RAW_IMU']['message'].ymag
        data['Z'] = self.messages['RAW_IMU']['message'].zmag
        return json.dumps(data)

    def getIMUData(self):
        '''Returns a JSON containing IMU Data'''
        self.log.debug('Fetching IMU Data')

        data = {}
        data['Magnetometer'] = json.loads(self.getMagnetometerData())
        data['Accelerometer'] = json.loads(self.getAccelerometerData())
        data['Gyroscope'] = json.loads(self.getGyroscopeData())
        return json.dumps(data)

    def getPressureExternal(self):
        ''' Returns the reading of the pressure sensor in Pascals '''

        self.log.debug('Fetching External Pressure')

        # Check message availability
        if not self.config['messages']['pressureSensorExternal'] in self.messages:
            self.log.warn('Scaled Pressure message not available, Possible config issue.')
            sleep(1)

        # Get the pressure data
        pressure_data = self.messages[self.config['messages']['pressureSensorExternal']].message
        self.log.debug(round(100 * float(pressure_data.press_abs), 2))
        return round(100 * float(pressure_data.press_abs), 2)   # convert to Pascals before returning

    def getDepth(self):
        '''Returns the depth of the drone in meters as a float'''
        self.log.debug('Fetching Depth')

        # Get variable values from config
        surfacePressure = int(self.config['geodata']['surfacePressure'])    # pascals
        fluidDensity = int(self.config['geodata']['fluidDensity'])          # kg/m^3
        g = 9.8066                                                          # m/s^2

        # Calculate depth
        depth = ((self.getPressureExternal() - surfacePressure) / (fluidDensity * g)) * -1
        self.log.debug('Depth = ' + str(depth))
        return round(depth, 2)    # Meters

    def getAltitude(self):
        '''
        Returns the distance between the sonar sensor and the ground
        Raises an exception if no sonar sensors are enabled.
        '''
        self.log.debug('fetching height')
        if int(self.config['hardware']['sonarcount']) == 0:
            # If there are no sonar sensors attached
            self.log.debug('Sonar disabled in config, raising exception')
            raise ResourceWarning("This drone does not have an enabled sonar sensor.\n"
                                  + "If the drone does have a sonar sensor, set the 'sonarcount' entry in the config")
        sonarData = self.sonar.getMessage()
        return (float(json.loads(sonarData)['distance']) / 1000)    # Convert to meters

    # Configuration Commands
    def setSurfacePressure(self, pressure=None):
        '''
        Sets the surface pressure (used in depth calculations) to the given value.
        If no value is given, uses the current external pressure of the drone

        parameter pressure: The pressure in pascals to make default. Sea Level is 101325
        '''
        if not pressure:
            pressure = self.getPressureExternal()
            self.log.info('Pressure not given, using current pressure of ' + str(pressure) +
                          '. Was ' + str(self.config['geodata']['surfacePressure']))
        else:
            self.log.info('Setting surface pressure to ' + str(pressure) +
                          '. Was ' + str(self.config['geodata']['surfacePressure']))

        pressure = round(pressure)  # Round to nearest int

        self.config.set('geodata', 'surfacePressure', str(pressure))
        # Write value to configFile
        with open(self.configPath, 'w') as configFile:
            self.config.write(configFile)

    def setFluidDensity(self, density=1000):
        '''
        Sets the fluid density (used in depth calculations) to the given value.
        If no value is given, 1000, the density of fresh water

        parameter density: The density of the liquid in which the drone is diving in kg/m^3.
        Freshwater is 1000, salt water is typically 1020-1030
        '''
        self.log.info('Setting fluidDensity to ' + str(density)
                      + '. Was ' + str(self.config['geodata']['fluidDensity']))

        self.config.set('geodata', 'fluidDensity', str(density))
        # Write value to configFile
        with open(self.configPath, 'w') as configFile:
            self.config.write(configFile)

    # Beta Commands
    def yawBeta(self, angle, rate=20, direction=1, relative=1, execMode=None):     # Broken
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees
        rate: rotational velocity in deg/s
        direction: 1 = Clockwise, -1 = CCW
        relative: (1) - zero is current bearing, (0) - zero is north
        '''
        t = Thread(target=commands.active.yawBeta,
                   args=(self.mavlinkConnection, self.sem, angle, rate, direction, relative,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def changeAltitude(self, rate, altitude, execMode=None):
        t = Thread(target=commands.active.changeAltitude, args=(self.mavlinkConnection, self.sem, rate, altitude,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def setLights(self, brightness, execMode=None):
        '''
        Set the lights of the drone to a certain level

        param brightness: the percentage of full brightness (rounded to the nearest step) to set the lights to
        '''
        t = Thread(target=self.lights.set, args=(self.mavlinkConnection, self.sem, brightness,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def wait(self, time, execMode=None):
        '''
        Pushes an input of zero so no action is taken. Possibly necessary when sleeping for more than 1 second

        param time: an integer representing the number of seconds to wait
        '''
        t = Thread(target=commands.active.wait, args=(self.mavlinkConnection, self.sem, time,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(self.execMode == 'synchronous'):
                t.join()   # Wait when using synchronous mode

    def getHeading(self):
        # mag_heading found in pymavlink.mavextra
        return mag_heading(self.messages['RAW_IMU']['message'], self.messages['ATTITUDE']['message'])
