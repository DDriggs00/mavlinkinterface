# from time import sleep  # For waiting between cycles
from mavlinkinterface.logger import getLogger

class dataRefresher(object):
    '''This class continuously gets data from pymavlink in order to clear the port'''
    def __init__(self, ml, message, killEvent, doLog):

        self.ml = ml
        self.message = message
        self.killEvent = killEvent
        self.doLog = doLog
        self.log = getLogger("dataRefresher")

        # Autostart this class upon initialization
        self.log.debug("dataRefresher Class Initiating for message " + message + ". Logging=" + str(doLog))
        self.refresh()

    def refresh(self):
        '''This function is the data gatherer'''
        while not self.killEvent.wait(o):
            # Add all message types that are used elsewhere
            self.ml.recv_match(type=self.message, blocking=True)           # Accel/Gyro/mag data
            # sleep(.1)
