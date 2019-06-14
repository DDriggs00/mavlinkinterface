from time import sleep  # For waiting between cycles

class dataRefresher(object):
    '''This class continuously gets data from pymavlink in order to prevent messages from sitting in the port'''
    def __init__(self, ml):
        self.__stop = False
        # Autostart this class upon initialization
        self.refresh(ml)

    def refresh(self, ml):
        '''This function is the data gatherer'''
        while not self.__stop:
            # Add all message types that are used elsewhere
            ml.recv_match(type="RAW_IMU", blocking=False)           # Accel/Gyro/mag data
            ml.recv_match(type="SCALED_PRESSURE", blocking=False)   # Pressure/temp
            ml.recv_match(type="SYS_STATUS", blocking=False)        # Battery
            sleep(.25)

    def kill(self):
        '''Stops the data gathering'''
        self.__stop = True
