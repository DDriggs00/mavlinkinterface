# External Imports
from time import sleep  # delay needed due to adjustment method
# Internal Imports
from mavlinkinterface.logger import getLogger   # For Logging


class lights(object):

    steps = 8   # number of brightness levels the light has

    def __init__(self):
        for i in range(0, self.steps):
            self.__down()
            sleep(0.05)
        self.level = 0
        self.log = getLogger("Lights")

    def set(self, ml, sem, brightness):
        self.log.info("Setting Lights to " + str(brightness) + "% brightness")
        try:
            desiredLevel = round(0.09 * brightness)
            self.log.debug("current lighting level = " + str(self.level))
            self.log.debug("desired lighting level = " + str(brightness))

            while desiredLevel > self.level:
                self.__up(ml)
                self.level += 1
                sleep(0.05)

            while desiredLevel < self.level:
                self.__down(ml)
                self.level -= 1
                sleep(0.05)
        finally:
            sem.release()

    def __up(self, ml):
        buttons = 1 << 14
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ Range: -1000-1000; backward=-1000, forward=1000, 0 = No X-Axis thrust ]
            0,          # y [ Range: -1000-1000; Left=-1000, Right=1000, 0 = No Y-Axis thrust ]
            500,        # z [ Range: 0-1000; 0=down, 1000=up; 500 = no vertical thrust ]
            0,          # r [ Yaw, with counter-clockwise being negative. ]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.05)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,    # x [ Range: -1000-1000; backward=-1000, forward=1000, 0 = No X-Axis thrust ]
            0,    # y [ Range: -1000-1000; Left=-1000, Right=1000, 0 = No Y-Axis thrust ]
            500,  # z [ Range: 0-1000; 0=down, 1000=up; 500 = no vertical thrust ]
            0,    # r [ Yaw, with counter-clockwise being negative. ]
            0)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]

    def __down(self, ml):
        buttons = 1 << 13
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ Range: -1000-1000; backward=-1000, forward=1000, 0 = No X-Axis thrust ]
            0,          # y [ Range: -1000-1000; Left=-1000, Right=1000, 0 = No Y-Axis thrust ]
            500,        # z [ Range: 0-1000; 0=down, 1000=up; 500 = no vertical thrust ]
            0,          # r [ Yaw, with counter-clockwise being negative. ]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.05)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,    # x [ Range: -1000-1000; backward=-1000, forward=1000, 0 = No X-Axis thrust ]
            0,    # y [ Range: -1000-1000; Left=-1000, Right=1000, 0 = No Y-Axis thrust ]
            500,  # z [ Range: 0-1000; 0=down, 1000=up; 500 = no vertical thrust ]
            0,    # r [ Yaw, with counter-clockwise being negative. ]
            0)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
