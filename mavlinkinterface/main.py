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
import atexit                           # For keeping the queue executing while a script ends

# Local Imports
from mavlinkinterface.logger import getLogger           # For Logging
import mavlinkinterface.commands as commands            # For calling commands
# from mavlinkinterface.rthread import RThread            # For functions that have return values

class mavlinkInterface(object):
    '''
    This is the main interface to Mavlink. All calls will be made through this object.
    '''

    configVersion = '1.1'

    # Internal Commands
    def __init__(self, execMode: str, sitl=False):
        '''
        Creates a new mavlinkInterface Object

        :param execMode: The Execution mode to use when not given as a parameter.
                         See docs/configuration/setDefaultexecMode for details.\n
        '''
        if execMode not in ['synchronous', 'queue', 'ignore', 'override']:
            raise ValueError('The execMode parameter must be one of the following:\n'
                             + ' synchronous, queue, ignore, override')

        # Initialize logger
        self.__log = getLogger('Main', doPrint=True)
        self.__log.trace('################################################################################')
        self.__log.trace('###################### New Log ' + str(datetime.now()) + ' ######################')
        self.__log.trace('################################################################################')

        # Import config values
        self.config = ConfigParser()
        self.configPath = abspath(expanduser('~/.mavlinkInterface.ini'))
        if exists(self.configPath):
            self.__log.trace('importing configuration file from path: ' + self.configPath)
            self.config.read(self.configPath)

        if (not exists(self.configPath)
                or 'version' not in self.config
                or self.config['version']['version'] != self.configVersion):

            # Populate file with Default config options
            self.config['version'] = {'version': self.configVersion}
            self.config['mavlink'] = {'connectionString': 'udp:0.0.0.0:14550'}
            self.config['geodata'] = {'COMMENT_1': 'The pressure in pascals at the surface of the body of water.',
                                      'COMMENT_1B': 'Sea Level is around 101325. Varies day by day',
                                      'surfacePressure': '101325',
                                      'COMMENT_2': 'The density of the diving medium. Pure water is 1000',
                                      'fluidDensity': '1000'}
            self.config['messages'] = {'refreshrate': '0.04',
                                       'controlRate': '.1'}
            self.config['hardware'] = {'sonarcount': '1',
                                       'gps': 'True'}
            # Save file
            self.config.write((open(self.configPath, 'w')))

        # Set class variables
        self.__log.trace('Setting class variables')
        self.execMode = execMode
        self.externalPressureMessage = 'SCALED_PRESSURE2'
        # Leak response action valid options:
        # "nothing": warns the user and takes note in the log, but takes no other action
        # "surface": raises the drone to the surface, overriding any existing commands
        # <absolute path to .py file, in specified format>
        self.leakResponseAction = 'surface'

        # Handle SITL Mode
        self.sitl = sitl
        if sitl:
            self.__log.warn('========================================')
            self.__log.warn('=========== SITL MODE ACTIVE ===========')
            self.__log.warn('========================================')
            self.externalPressureMessage = 'SCALED_PRESSURE'

        # Create variables to contain mavlink message data
        self.messages = {}

        self.gpsEnabled = bool(self.config['hardware']['gps'])

        # Create Semaphore and Queue
        self.sem = Semaphore(1)
        self.q = Queue()

        # Set up Mavlink
        self.__log.trace('Initializing MavLink Connection')
        self.mavlinkConnection = mavutil.mavlink_connection(self.config['mavlink']['connectionString'])
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

        # Set messages to be read
        self.readMessages = ['SYS_STATUS',
                             'RAW_IMU',
                             'SCALED_PRESSURE',
                             'SCALED_PRESSURE2',
                             'HEARTBEAT',
                             'ATTITUDE',
                             'STATUSTEXT']
        if self.gpsEnabled:
            self.readMessages.append('GPS_RAW_INT')              # Basic GPS
            self.readMessages.append('GLOBAL_POSITION_INT')      # Advanced GPS
            self.readMessages.append('MISSION_REQUEST')          # For missions
            self.readMessages.append('MISSION_ACK')              # For missions
            self.readMessages.append('MISSION_ITEM')             # For missions
            self.readMessages.append('MISSION_ITEM_REACHED')     # For missions
            self.readMessages.append('MISSION_CURRENT')          # For missions
            self.readMessages.append('EKF_STATUS_REPORT')        # For GPS and missions

        # start dataRefreshers
        self.recordedMessages = {
            'GPS_RAW_INT': 0,
            'SCALED_PRESSURE2': 0
        }
        self.refresher = Thread(target=self.__updateMessage, args=(self.killEvent,))
        self.refresher.daemon = True    # Kill on program end
        self.refresher.start()

        # start heartbeat maintainer
        self.heartbeatThread = Thread(target=self.__heartbeatMaintain, args=(self.killEvent,))
        self.heartbeatThread.daemon = True  # Kill on program end
        self.heartbeatThread.start()

        # start Manual control process
        self.manualControlParams = {
            'x': 0,     # X-Axis thrust [Range: -1000-1000; Back=-1000, Forward=1000, 0 = No 'forward' thrust]
            'y': 0,     # Y-Axis thrust [Range: -1000-1000; Left=-1000, Right=1000, 0 = No 'sideways' thrust]
            'z': 500,   # Z-Axis thrust [Range: -1000-1000; Left=-1000, Up=1000, 500 = No vertical thrust]
            'r': 0,     # Rotation [Range: -1000-1000; Left=-1000, Right=1000, 0 = No rotational thrust]
            'b': 0      # A bitfield representing controller buttons pressed,(use 1 << btn# to activate button)
        }
        self.manualControlThread = Thread(target=self.__manualControlMaintain, args=(self.killEvent,))
        self.manualControlThread.daemon = True  # Kill on program end
        self.manualControlThread.start()

        # start leak detection
        self.leakDetectorThread = Thread(target=self.__leakDetector, args=(self.killEvent,))
        self.leakDetectorThread.daemon = True   # Kill on program end
        self.leakDetectorThread.start()

        # Start Queue maintenance process
        self.queueThread = Thread(target=self.__queueManager, args=(self.killEvent,))
        self.queueThread.daemon = True   # Kill on program end
        self.queueThread.start()

        # Start message recording process
        self.dataRecorderThread = Thread(target=self.__dataRecorder, args=(self.killEvent,))
        self.dataRecorderThread.daemon = True   # Kill on program end
        self.dataRecorderThread.start()

        # Initiate light class
        self.lights = commands.active.lights(self)

        # Initiate sonar class
        if int(self.config['hardware']['sonarcount']) > 0:
            self.sonar = commands.passive.sonar()

        if self.gpsEnabled:
            self.gps = commands.passive.gps(self)

        # Validating heartbeat
        self.__log.info('Waiting for heartbeat')
        while 'HEARTBEAT' not in self.messages:
            sleep(.1)
        self.__log.info('Successfully connected to target.')
        self.__log.trace('__init__ end')

        atexit.register(self.waitQueue)

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
        except (NameError, AttributeError):
            pass    # Initializer not finished, so no need to clean up after it

    # Private functions
    def __getSemaphore(self, mode: str, target: Thread) -> bool:
        '''
        Attempts to acquire the movement semaphore based on execMode.
        Returns true if semaphore was acquired, false otherwise.
        '''

        if mode is None:
            mode = self.execMode

        if not self.sem.acquire(blocking=False):    # Semaphore could not be acquired, proceeding by mode

            if mode == 'synchronous':
                self.__log.info('QueueMode = synchronous, waiting for queue and semaphore')
                try:
                    while self.q.qsize() > 0:
                        sleep(.1)
                    self.sem.acquire(blocking=True)
                except KeyboardInterrupt:
                    self.__log.error('Keyboard interrupt received, aborting command')
                    return False

                return True

            if mode == 'override':
                self.__log.info('Override active, Killing existing task(s)')
                self.stopAllTasks()
                if not self.sem.acquire(blocking=False):    # If the current task did not properly release the semaphore
                    self.sem.release()                      # Release it
                    self.sem.acquire()                      # Then re-take it
                return True     # Now that previous action has been killed, execute current action
            elif self.execMode == 'ignore':
                self.__log.info('Using Ignore mode, command ignored')
                return False    # The command should not be executed

            elif self.execMode == 'queue':
                self.__log.info('Using queue Mode, Adding item to queue')
                self.q.put(target)
                return False    # The command will be executed by the QueueManager process
        return True     # If the semaphore was obtained on the first try

    def __updateMessage(self, killEvent: Event) -> None:
        '''
        This function automatically updates a variable to contain the contents of a mavlink message

        :param killEvent: set killEvent event to end this thread
        '''
        log = getLogger('Refresh')  # Log that this was started
        log.trace('dataRefresher Class Initiating.')

        filePath = abspath(expanduser("~/logs/mavlinkInterface/"))

        files = {}
        for m in self.readMessages:
            if m in self.recordedMessages:
                files[m] = open(filePath + '/' + m + '.log', 'a+')

        while not killEvent.is_set():   # When killEvent is set, stop looping
            msg = None
            msg = self.mavlinkConnection.recv_match(type=self.readMessages, blocking=True, timeout=1)

            # Timeout used so it has the chance to notice the stop flag when no data is present
            if msg:
                self.messages[str(msg.get_type())] = {'message': msg, 'time': datetime.now()}
                if msg.get_type() in self.recordedMessages and self.recordedMessages[msg.get_type()] == 0:
                    files[msg.get_type()].write(str(datetime.now()) + ', ' + str(msg.to_dict()) + '\n')

    def __leakDetector(self, killEvent: Event) -> None:
        '''This function continuously checks for leaks, and upon detecting a leak, runs the desired action'''
        log = getLogger('Status', doPrint=True)
        log.trace('Leak Detector started')
        while not killEvent.wait(timeout=1):
            if 'STATUSTEXT' in self.messages and 'LEAK' in str(self.messages['STATUSTEXT']['message']).upper():
                log.error('Leak Detected: ' + self.messages['STATUSTEXT']['message'])    # Write the message to the log
                self.leakResponse()

        log.trace('StatusMonitor Stopping')

    def __heartbeatSend(self,
                        type: int = 6,
                        autopilot: int = 8,
                        base_mode: int = 192,
                        custom_mode: int = 0,
                        system_status: int = 4,
                        mavlink_version: int = 3) -> None:
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

    def __manualControlSend(self) -> None:
        '''
        Sends a manual control message based on the dict self.manualControlParams

        Detailed description of MANUAL_CONTROL Message
        Name: MANUAL_CONTROL ( #69 )
        Usage: This message provides an API for manually controlling the vehicle using standard joystick axes.
        It is typically used with a joystick-like input device, but can also be used for other forms of manual control.
        X, Y, Z, and r axes can be disabled with a value of INT16_MAX (Not used in this case).

        Field Name  Type	    Description
        x	        int16_t	    X-Axis thrust/Pitch [Range: -1000-1000; Back=-1000, Forward=1000, 0 = No thrust]
        y	        int16_t	    Y-Axis thrust/Roll [Range: -1000-1000; Left=-1000, Right=1000, 0 = No thrust]
        z	        int16_t	    Z-Axis thrust/Lift [Range: -1000-1000; Left=-1000, Up=1000, 500 = No thrust]
        r	        int16_t	    R-axis Thrust/Rotation [Range: -1000-1000; Left=-1000, Right=1000, 0 = No thrust]
        buttons	    uint16_t	A bitfield representing controller buttons pressed,(use 1 << btn# to activate button)
        '''
        self.mavlinkConnection.mav.manual_control_send(
            self.mavlinkConnection.target_system,
            self.manualControlParams['x'],  # X-Axis thrust
            self.manualControlParams['y'],  # Y-Axis thrust
            self.manualControlParams['z'],  # Z-Axis thrust
            self.manualControlParams['r'],  # R-Axis thrust
            self.manualControlParams['b']   # Button bitmap
        )

    def __heartbeatMaintain(self, killEvent: Event) -> None:
        '''This function continuously sends a heartbeat message'''
        self.__log.trace('Heartbeat broadcast started')
        while not killEvent.wait(timeout=1):
            self.__heartbeatSend()
        self.__log.trace('Heartbeat broadcast stopped')

    def __manualControlMaintain(self, killEvent: Event) -> None:
        '''This function continuously sends the manual_control message'''
        self.__log.trace('Manual Control broadcast started')
        while not killEvent.wait(timeout=(float(self.config['messages']['controlRate']))):
            self.__manualControlSend()
        self.__log.trace('Manual Control broadcast stopped')

    def __dataRecorder(self, killEvent: Event) -> None:
        '''
        This function logs data to a file when the logging is set to log at an interval.
        '''

        filePath = abspath(expanduser("~/logs/mavlinkInterface/"))
        files = {}
        for m in self.readMessages:
            files[m] = open(filePath + '/' + m + '.log', 'a+')
        i = 0

        while not killEvent.wait(.5):

            for message in self.recordedMessages:
                if self.recordedMessages[message] > 0 and (i % (2 * self.recordedMessages[message])) == 0:
                    if message in self.messages:
                        files[message].write(str(datetime.now()) + ', ' + str(self.messages[message]['message']) + '\n')
                        files[message].flush()

            if i == 120:
                i = 0

            i += 1

    def __queueManager(self, killEvent: Event) -> None:
        self.__log.trace('queueManager starting')
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
    def stopAllTasks(self) -> None:
        # Clear Queue
        while self.q.qsize() > 0:
            self.q.get(block=False)
        self.stopCurrentTask()

    def stopCurrentTask(self) -> None:
        # Kills the currently running task and stops the drone
        self.currentTaskKillEvent.set()

    def log(self, message: str) -> None:
        '''This function writes a message to the program log'''
        self.__log.trace(message)

    def waitQueue(self) -> None:
        '''
        This blocks until the current queue has finished executing.
        This function has no other function
        '''
        self.__log.info('Waiting for queue')
        try:
            # Wait for queue
            while self.q.qsize() > 0:
                sleep(.1)

            # Wait for last item to execute
            if self.sem.acquire(blocking=True):
                self.sem.release()

        except KeyboardInterrupt:
            # Interrupted by Ctrl+C
            self.__log.warn('Keyboard interrupt received, aborting command')

    def leakResponse(self) -> None:
        '''
        This function is called upon encountering a leak.
        '''
        self.__log.warn('Leak response triggered')
        print('Leak detected, performing appropriate action')
        self.__log.trace('Leak response is ' + self.leakResponseAction)

        if self.leakResponseAction == 'surface':
            self.surface(execMode='override')

        elif self.leakResponseAction in ['nothing', 'warn', 'none']:
            self.__log.warn('Leak Action is set to warn only, no further action will be taken')

        elif self.leakResponseAction == 'home':
            self.__log.warn('the home action is not yet implemented, surfacing instead')
            self.surface(execMode='override')

        else:
            self.__log.warn('the custom script action is not yet implemented, surfacing instead')
            self.surface(execMode='override')

    def disableSensor(self, sensor: str, enable: bool = False) -> None:
        validSensors = ['pressure', 'gps', 'sonar']
        if sensor not in validSensors:
            self.__log.error('Invalid option.  Valid options are: ' + str(validSensors))
            return
        if sensor == 'pressure':
            if self.externalPressureMessage in self.readMessages:
                if enable:
                    self.readMessages.append(self.externalPressureMessage)
                else:
                    self.readMessages.remove(self.externalPressureMessage)
        elif sensor == 'gps':
            if 'GPS_RAW_INT' in self.readMessages:
                if enable:
                    self.readMessages.append('GPS_RAW_INT')
                else:
                    self.readMessages.remove('GPS_RAW_INT')
            if 'GLOBAL_POSITION_INT' in self.readMessages:
                if enable:
                    self.readMessages.append('GLOBAL_POSITION_INT')
                else:
                    self.readMessages.remove('GLOBAL_POSITION_INT')
        elif sensor == 'sonar':
            if int(self.config['hardware']['sonarcount']) > 0:
                if enable:
                    self.sonar.disabled = False
                else:
                    self.sonar.disabled = True

    # Active commands
    def arm(self, execMode: str = None) -> None:
        '''Enables the thrusters'''

        # Create thread object
        t = Thread(target=commands.active.arm, args=(self.mavlinkConnection, self.sem))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):    # If sem was able to be acquired
            t.start()                     # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def disarm(self, execMode: str = None) -> None:
        '''Disables the thrusters'''

        t = Thread(target=commands.active.disarm, args=(self.mavlinkConnection, self.sem,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):    # If sem was able to be acquired
            t.start()                     # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def setFlightMode(self, flightMode: str, execMode: str = None) -> None:
        '''
        Sets the flight mode of the drone.
        Valid modes are listed in docs/active/setFlightMode.md

        Parameter Mode: The mode to use
        '''
        t = Thread(target=commands.active.setFlightMode, args=(self.mavlinkConnection, self.sem, flightMode,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def move(self,
             direction: float,
             time: float,
             throttle: int = 50,
             absolute: bool = False,
             execMode: str = None) -> None:
        '''
        Move horizontally in any direction

        Parameter Direction: the angle (in degrees) to move toward
        Parameter time: the time (in seconds) to power the thrusters
        Parameter throttle: the percentage of thruster power to use
        Parameter Absolute: When true, an angle of 0 degrees is magnetic north
        '''
        t = Thread(target=commands.active.move,
                   args=(self.manualControlParams, self.sem, self.currentTaskKillEvent, direction, time, throttle,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def move3d(self, throttleX: int, throttleY: int, throttleZ: int, time: float, execMode: str = None) -> None:
        '''
        Move in any direction

        Parameter Throttle X: Percent power to use when thrusting in the X direction
        Parameter Throttle Y: Percent power to use when thrusting in the Y direction
        Parameter Throttle Z: Percent power to use when thrusting in the Z direction
        Parameter Time: The time (in seconds) to power the thrusters
        '''
        t = Thread(target=commands.active.move3d,
                   args=(self.manualControlParams, self.sem, self.currentTaskKillEvent,
                         throttleX, throttleY, throttleZ, time,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def dive(self, depth: float, throttle: int = 50, absolute: bool = False, execMode: str = None) -> None:
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
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def diveTime(self, time: float, throttle: int, execMode: str = None) -> None:
        '''
        Thrust vertically for a specified amount of time

        :param time: how long to thrust in seconds
        :param throttle: percent throttle to use, -100 = full down, 100 = full up
        '''
        t = Thread(target=commands.active.diveTime,
                   args=(self.manualControlParams, self.sem, self.currentTaskKillEvent, time, throttle,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def surface(self, execMode: str = None) -> None:
        '''
        Thrust upward at full power until reaching the surface
        '''
        t = Thread(target=commands.active.surface, args=(self, self.currentTaskKillEvent,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def yaw(self, angle: float, absolute=False, execMode: str = None) -> None:
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees
        '''
        t = Thread(target=commands.active.yaw,
                   args=(self, self.currentTaskKillEvent, angle, absolute,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def yawBasic(self, angle: float, absolute=False, execMode: str = None) -> None:
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees
        '''
        t = Thread(target=commands.active.yawBasic,
                   args=(self.manualControlParams, self.sem, self.currentTaskKillEvent, angle, absolute,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def gripperOpen(self, time: float, execMode: str = None) -> None:
        '''
        Opens the Gripper Arm
        '''
        t = Thread(target=commands.active.gripperOpen, args=(self.manualControlParams, self.sem, time,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def gripperClose(self, time: float, execMode: str = None) -> None:
        '''
        Closes the Gripper Arm
        '''
        t = Thread(target=commands.active.gripperClose, args=(self.manualControlParams, self.sem, time,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def setLights(self, brightness: int, execMode: str = None) -> None:
        '''
        Set the lights of the drone to a certain level

        param brightness: the percentage of full brightness (rounded to the nearest step) to set the lights to
        '''
        t = Thread(target=self.lights.set, args=(self, self.sem, brightness,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def wait(self, time: float, execMode: str = None) -> None:
        '''
        Pushes an input of zero so no action is taken. Possibly necessary when sleeping for more than 1 second

        param time: an integer representing the number of seconds to wait
        '''
        t = Thread(target=commands.active.wait,
                   args=(self.manualControlParams, self.sem, self.currentTaskKillEvent, time,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    # Sensor reading commands
    def getBatteryData(self) -> str:
        '''Returns a JSON-formatted string containing battery data'''
        self.__log.trace('Fetching battery data')

        # Check message availability
        if 'SYS_STATUS' not in self.messages:
            self.__log.warn('SYS_STATUS message not available, waiting 1 sec')
            sleep(1)

        data = {}
        data['voltage'] = self.messages['SYS_STATUS']['message'].voltage_battery / 1000        # convert to volts
        data['current'] = self.messages['SYS_STATUS']['message'].current_battery
        data['percent_remaining'] = self.messages['SYS_STATUS']['message'].battery_remaining
        return json.dumps(data)

    def getAccelerometerData(self) -> str:
        '''Returns a Json-formatted string containing Accelerometer Data'''
        self.__log.trace('Fetching Accelerometer Data')

        # Checking message availability
        if 'RAW_IMU' not in self.messages:
            self.__log.warn('RAW_IMU message not available, waiting 1 sec')
            sleep(1)

        data = {}
        data['X'] = self.messages['RAW_IMU']['message'].xacc
        data['Y'] = self.messages['RAW_IMU']['message'].yacc
        data['Z'] = self.messages['RAW_IMU']['message'].zacc
        return json.dumps(data)

    def getGyroscopeData(self) -> str:
        '''Returns a Json-formatted string containing Gyroscope Data'''
        self.__log.trace('Fetching Gyro Data')

        # Checking message availability
        if not self.messages.__contains__('RAW_IMU'):
            self.__log.warn('RAW_IMU message not available, waiting 1 sec')
            sleep(1)

        data = {}
        data['X'] = self.messages['RAW_IMU']['message'].xgyro
        data['Y'] = self.messages['RAW_IMU']['message'].ygyro
        data['Z'] = self.messages['RAW_IMU']['message'].zgyro
        return json.dumps(data)

    def getMagnetometerData(self) -> str:
        '''Returns a Json-formatted string containing Magnetometer Data'''
        self.__log.trace('Fetching magnetometer Data')
        if not self.messages.__contains__('RAW_IMU'):
            self.__log.warn('RAW_IMU message not available, waiting 1 sec')
            sleep(1)

        data = {}
        data['X'] = self.messages['RAW_IMU']['message'].xmag
        data['Y'] = self.messages['RAW_IMU']['message'].ymag
        data['Z'] = self.messages['RAW_IMU']['message'].zmag
        return json.dumps(data)

    def getIMUData(self) -> str:
        '''Returns a Json-formatted string containing IMU Data'''
        self.__log.trace('Fetching IMU Data')

        data = {}
        data['Magnetometer'] = json.loads(self.getMagnetometerData())
        data['Accelerometer'] = json.loads(self.getAccelerometerData())
        data['Gyroscope'] = json.loads(self.getGyroscopeData())
        return json.dumps(data)

    def getPressureExternal(self) -> float:
        '''Returns the reading of the pressure sensor in Pascals'''

        self.__log.trace('Fetching External Pressure')

        # Check message availability
        if self.externalPressureMessage not in self.messages:
            sleep(1)

        # Get the pressure data
        pressure_data = self.messages[self.externalPressureMessage]['message']
        self.__log.rdata(round(100 * float(pressure_data.press_abs), 2))
        return round(100 * float(pressure_data.press_abs), 2)   # convert to Pascals before returning

    def getPressureInternal(self) -> float:
        '''Returns the reading of the internal pressure sensor in Pascals'''

        self.__log.trace('Fetching External Pressure')

        # Check message availability
        if 'SCALED_PRESSURE' not in self.messages:
            sleep(1)

        # Get the pressure data
        pressure_data = self.messages['SCALED_PRESSURE']['message']
        self.__log.rdata('getInternalPressure about to return ' + str(round(100 * float(pressure_data.press_abs), 2)))
        return round(100 * float(pressure_data.press_abs), 2)   # convert to Pascals before returning

    def getDepth(self) -> float:
        '''Returns the depth of the drone in meters as a float'''
        self.__log.trace('Fetching Depth')

        # Get variable values from config
        surfacePressure = int(self.config['geodata']['surfacePressure'])    # pascals
        fluidDensity = int(self.config['geodata']['fluidDensity'])          # kg/m^3
        g = 9.8066                                                          # m/s^2

        # Calculate depth
        depth = ((self.getPressureExternal() - surfacePressure) / (fluidDensity * g)) * -1
        self.__log.trace('Depth = ' + str(depth))
        return round(depth, 2)    # Meters

    def getTemperature(self) -> float:
        '''
        Returns the reading of the Temperature sensor in degrees Celsius
        Note that the returned value is accurate only to the nearest degree
        '''

        self.__log.trace('Fetching Temperature from pressure sensor')

        # Check message availability
        if self.externalPressureMessage not in self.messages:
            self.__log.warn('Scaled Pressure message not available, Possible config issue.')
            sleep(1)

        # Get the pressure data
        pressure_data = self.messages[self.externalPressureMessage]['message']
        tempC = float(pressure_data.temperature) / 100.0
        self.__log.trace('getTemperature returning ' + str(tempC))
        return tempC

    def getAltitude(self) -> str:
        '''
        Returns the distance between the sonar sensor and the ground in meters (incl. confidence)
        Raises an exception if no sonar sensors are enabled.
        '''
        self.__log.trace('fetching height')
        if int(self.config['hardware']['sonarcount']) == 0:
            # If there are no sonar sensors attached
            self.__log.trace('Sonar disabled in config, raising exception')
            raise ResourceWarning("This drone does not have an enabled sonar sensor.\n"
                                  + "If the drone does have a sonar sensor, set the 'sonarcount' entry in the config")
        sonarData = json.loads(self.sonar.getMessage())
        if 'distance' not in sonarData:
            self.__log.error('A distance field was not found in the JSON.'
                             + ' This may be caused by another entity requesting and retrieving from the sensor')
            raise AttributeError("Distance not found in value returned from sonar sensor")
        # Restructure the output before returning
        returnData = {
            'altitude': str(float(sonarData['distance']) / 1000),
            'confidence': sonarData['confidence']
        }
        returnJson = json.dumps(returnData)
        self.__log.trace('getAltitude now returning ' + returnJson)
        return returnJson

    def getHeading(self) -> float:
        '''
        Returns the current heading of the drone based on compass data
        '''
        # mag_heading found in pymavlink.mavextra
        return mag_heading(self.messages['RAW_IMU']['message'], self.messages['ATTITUDE']['message'])

    # Configuration Commands
    def setSurfacePressure(self, pressure: float = None) -> None:
        '''
        Sets the surface pressure (used in depth calculations) to the given value.
        If no value is given, uses the current external pressure of the drone

        parameter pressure: The pressure in pascals to make default. Sea Level is 101325
        '''
        if not pressure:
            pressure = self.getPressureExternal()
            self.__log.info('Pressure not given, using current pressure of ' + str(pressure)
                            + '. Was ' + str(self.config['geodata']['surfacePressure']))
        else:
            self.__log.info('Setting surface pressure to ' + str(pressure)
                            + '. Was ' + str(self.config['geodata']['surfacePressure']))

        pressure = round(pressure)  # Round to nearest int

        self.config.set('geodata', 'surfacePressure', str(pressure))
        # Write value to configFile
        with open(self.configPath, 'w') as configFile:
            self.config.write(configFile)

    def setFluidDensity(self, density: float = 1000) -> None:
        '''
        Sets the fluid density (used in depth calculations) to the given value.
        If no value is given, 1000, the density of fresh water

        parameter density: The density of the liquid in which the drone is diving in kg/m^3.
        Freshwater is 1000, salt water is typically 1020-1030
        '''
        self.__log.info('Setting fluidDensity to ' + str(density)
                        + '. Was ' + str(self.config['geodata']['fluidDensity']))

        self.config.set('geodata', 'fluidDensity', str(density))
        # Write value to configFile
        with open(self.configPath, 'w') as configFile:
            self.config.write(configFile)

    def setDefaultExecMode(self, mode: str) -> None:
        '''
        Sets the default execution mode to be used when no mode is passed with a command.
        Allowed modes are:

        - 'queue'
        - 'override'
        - 'ignore'
        - 'synchronous'

        NOTE: This command may only be called when no commands are executing or queued
        '''

        self.__log.trace('setting default execution mode to ' + mode)

        if mode not in ['synchronous', 'queue', 'ignore', 'override']:
            self.__log.error("setDefaultExecMode failed: invalid mode")
            raise ValueError('The execMode parameter must be one of the following:\n'
                             + ' synchronous, queue, ignore, override')

        if self.q.qsize() > 0:
            self.__log.error("setDefaultExecMode failed: queue must be empty")
            raise ResourceWarning('Failed: queue must be empty')

        if not self.sem.acquire(blocking=False):
            self.__log.error("setDefaultExecMode failed: There must not be any currently executing commands")
            raise ResourceWarning('Failed: There must not be any currently executing commands')
        else:
            self.sem.release()

        self.execMode = mode
        self.__log.debug('Execution mode successfully set to ' + mode)

    def setLeakAction(self, action: str) -> None:
        '''
        Sets the leak response action. Valid values:

        - warn
        - surface
        - home (not yet implemented)
        - <path to a specified file, see documentation for details> (not yet implemented)
        '''
        self.__log.debug('Leak Action changed to ' + action)
        self.leakResponseAction = action

    # Beta Commands
    def yawBeta(self,
                angle: float,
                rate: float = 20,
                direction: bool = 1,
                relative: bool = 1,
                execMode: str = None) -> None:
        # THIS IS BROKEN TODO FIX
        '''Rotates the drone around the Z-Axis

        angle: distance to rotate in degrees
        rate: rotational velocity in deg/s
        direction: 1 = Clockwise, -1 = CCW
        relative: (1) - zero is current bearing, (0) - zero is north
        '''
        t = Thread(target=commands.active.yawBeta,
                   args=(self.mavlinkConnection,
                         self.sem,
                         self.currentTaskKillEvent,
                         angle,
                         rate,
                         direction,
                         relative,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def changeAltitude(self, rate, altitude, execMode: str = None) -> None:
        t = Thread(target=commands.active.changeAltitude, args=(self.mavlinkConnection, self.sem, rate, altitude,))

        # Calculate action based on mode
        if self.__getSemaphore(execMode, t):   # If sem was able to be acquired
            t.start()                 # Start the thread
            if(execMode == 'synchronous' or (execMode is None and self.execMode == 'synchronous')):
                t.join()   # Wait when using synchronous mode

    def setRecordingInterval(self, message: str, interval: int) -> None:
        '''
        Enables, Disables, or alters the interval at which data is recorded to a file.

        :param message (str): the mavlink message to record
        :param interval (int): the interval at which to record (every n seconds): -1=disabled, 0=every message
        Resolution of 0.5 sec, Maximum interval of 60 seconds
        '''
        # Round interval to the nearest sec
        interval = round(2 * interval) / 2

        # enforce max interval
        if interval > 60:
            interval = 60

        # if not list, convert to list
        if not isinstance(message, list):
            message = [message]

        for msg in message:
            self.__log.info("setting " + msg + ' recording interval to ' + str(interval))

            if interval < 0:
                # Disable recording for message
                self.__log.trace('Disabling recording of ' + msg)
                self.recordedMessages.pop(msg, None)

            else:
                self.__log.trace('setting recording of ' + msg + ' to log a message '
                                 + 'at intervals of ' + str(interval))
                self. recordedMessages[msg] = interval
