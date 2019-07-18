from time import sleep
from pymavlink import mavutil, mavwp
from mavlinkinterface.logger import getLogger


class mission(object):
    '''A Mission that will have items added to it, then sent to the drone for completion
    To use a mission, perform the following steps:

    1. Create a mission object
    2. Add mission commands to the mission
    3. start the mission
    4. wait for the mission to complete
    '''
    # Based on https://discuss.ardupilot.org/t/33610
    def __init__(self, mli):

        # Keep pointer to main class
        self.__mli = mli
        self.__log = getLogger('Mission')
        # Create pymavlink waypoint loader
        self.wp = mavwp.MAVWPLoader()

        # Initialize message counter to 1
        self.seq = 1

        # idk, but it's important. probably absolute vs relative altitude
        self.__frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT

        # First command must be setHome TODO: figure out why
        self.setHome()

    def setHome(self, lat: float = None, lon: float = None) -> None:
        '''Sets the GPS Home position to the given coordinates (or the current position if none are given)

        :param lat: the latitude to set as home in decimal degrees (use at least 6 decimal places)
        :param lon: the longitude to set as home in decimal degrees (use at least 6 decimal places)
        Note: if either lat or lon is present, both must be present
        '''

        if lat is None and lon is None:
            current = 1
            self.__log.debug('Adding command to set Home to current location')
        elif lat is not None and lon is not None:
            current = 0
            self.__log.debug('Adding command to set Home to ' + str(lat) + ', ' + str(lon))
        else:
            print("Coordinates may only be passed in pairs, command ignored")
            return

        self.wp.add(mavutil.mavlink.MAVLink_mission_item_message(
            self.__mli.mavlinkConnection.target_system,
            self.__mli.mavlinkConnection.target_component,
            self.seq,
            self.__frame,
            mavutil.mavlink.MAV_CMD_DO_SET_HOME,    # Command
            0,          # "waypoint.current"
            0,          # "waypoint.autocontinue"
            current,    # param1 current, 1 = current, 0 = specified
            0,          # param2 Ignored
            0,          # param3 Ignored
            0,          # param4 Ignored
            0,          # param5 Latitude
            0,          # Param6 Longitude
            0))         # Param7 Altitude

        self.seq += 1   # seq number must be incremented after each added command

    def goToCoordinates(self, lat: float, lon: float) -> None:
        '''Adds the given coordinates to the mission plan as a stop

        :param lat: the latitude to set as home in decimal degrees (use at least 6 decimal places)
        :param lon: the longitude to set as home in decimal degrees (use at least 6 decimal places)
        '''
        self.__log.debug('Adding command to move to ' + str(lat) + ', ' + str(lon))

        self.wp.add(mavutil.mavlink.MAVLink_mission_item_message(
            self.__mli.mavlinkConnection.target_system,
            self.__mli.mavlinkConnection.target_component,
            self.seq,
            self.__frame,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,   # Command
            0,      # "waypoint.current"
            0,      # "waypoint.autocontinue"
            0,      # param1 Hold time (copter/rover only)
            0,      # param2 Acceptance Radius (m) (plane only)
            0,      # param3 Orbit distance (0 for pass through)
            0,      # param4 Desired yaw at target
            lat,    # param5 Latitude
            lon,    # Param6 Longitude
            0))     # Param7 Altitude

        self.seq += 1   # seq number must be incremented after each added command

    def upload(self) -> None:
        '''Uploads the flight plan to the drone. This will overwrite any previous flight plans.'''

        # remove previous missions
        self.__mli.mavlinkConnection.waypoint_clear_all_send()

        # Notify drone of mission length
        self.__mli.mavlinkConnection.waypoint_count_send(self.wp.count())

        missionSeq = -1     # for keeping track of messages

        # for each mission:
        for i in range(self.wp.count()):

            # Wait for acknowledgement
            while 'MISSION_REQUEST' not in self.__mli.messages:
                sleep(.1)
            msg = self.__mli.messages['MISSION_REQUEST']['message']
            while msg.seq == missionSeq:
                sleep(.1)
                msg = self.__mli.messages['MISSION_REQUEST']['message']
            missionSeq = msg.seq

            # Send command
            self.__mli.mavlinkConnection.mav.send(self.wp.wp(msg.seq))

    def start(self, wait: bool = False) -> None:
        '''Starts the mission that was most recently uploaded to the drone

        Note: The mission this starts may not be this mission.
        '''
        self.__mli.mavlinkConnection.mav.command_long_send(
            self.__mli.mavlinkConnection.target_system,
            self.__mli.mavlinkConnection.target_component,
            mavutil.mavlink.MAV_CMD_MISSION_START,
            0,  # Confirmation
            0,  # param1: First mission item to execute
            self.wp.count() - 1,  # param2: Last mission item to execute
            0,  # param3: Meaningless
            0,  # param4: Meaningless
            0,  # param5: Meaningless
            0,  # param6: Meaningless
            0)  # param7: Meaningless

        if wait:
            while 'MISSION_ITEM_REACHED' not in self.__mli.messages:
                sleep(.1)
            msg = self.__mli.messages['MISSION_ITEM_REACHED']['message']
            while msg.seq == self.wp.count():
                sleep(.5)
                msg = self.__mli.messages['MISSION_REQUEST']['message']
