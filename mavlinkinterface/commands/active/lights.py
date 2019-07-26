# External Imports
from time import sleep  # delay needed due to adjustment method
# Internal Imports
from mavlinkinterface.logger import getLogger   # For Logging


class lights(object):

    steps = 8   # number of brightness levels the light has

    def __init__(self, mli):
        for i in range(0, self.steps):
            self.__down(mli)
            sleep(0.04)
        self.level = 0
        self.log = getLogger("Lights")

    def set(self, mli, sem, brightness):
        if brightness > 100 or brightness < 0:
            self.log.warn('Brightness must be from 0 to 100')

        self.log.info("Setting Lights to " + str(brightness) + "% brightness")
        try:
            desiredLevel = round(0.09 * brightness)
            self.log.trace("current lighting level = " + str(self.level))
            self.log.trace("desired lighting level = " + str(brightness))

            while desiredLevel > self.level:
                self.__up(mli)
                self.level += 1
                sleep(0.05)

            while desiredLevel < self.level:
                self.__down(mli)
                self.level -= 1
                sleep(0.05)
        finally:
            sem.release()

    def __up(self, mli):

        # Because the 
        mli.mavlinkConnection.mav.manual_control_send(
            mli.mavlinkConnection.target_system,
            mli.manualControlParams['x'],  # X-Axis thrust
            mli.manualControlParams['y'],  # Y-Axis thrust
            mli.manualControlParams['z'],  # Z-Axis thrust
            mli.manualControlParams['r'],  # R-Axis thrust
            (mli.manualControlParams['b'] | 1 << 14)
        )
        sleep(0.05)

    def __down(self, mli):

        mli.mavlinkConnection.mav.manual_control_send(
            mli.mavlinkConnection.target_system,
            mli.manualControlParams['x'],  # X-Axis thrust
            mli.manualControlParams['y'],  # Y-Axis thrust
            mli.manualControlParams['z'],  # Z-Axis thrust
            mli.manualControlParams['r'],  # R-Axis thrust
            (mli.manualControlParams['b'] | 1 << 13)
        )
        sleep(0.05)
