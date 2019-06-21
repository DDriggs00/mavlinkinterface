from time import sleep

from mavlinkinterface.logger import getLogger

class lights(object):

    steps = 8

    def __init__(self):
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
                sleep(0.1)

            while desiredLevel < self.level:
                self.__down(ml)
                self.level -= 1
                sleep(0.1)
        finally:
            sem.release()

    def __up(self, ml):
        buttons = 1 << 14
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.1)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            0)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]

    def __down(self, ml):
        buttons = 1 << 13
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.25)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            0)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
