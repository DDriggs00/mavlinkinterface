from threading import currentThread             # For the ability to stop

from mavlinkinterface.logger import getLogger   # For Logging

class statusMonitor(object):
    '''This class performs the following tasks.
    (1): Reports all STATUSTEXT to the user and the log
    (2): Upon detecting a leak, runs the leakAction function'''
    def __init__(self, MLI, killEvent):

        self.killEvent = killEvent
        self.t = currentThread()
        self.log = getLogger("Status")
        self.log.debug("Status monitor started")
        # Autostart this class upon initialization
        self.refresh(MLI)

    def refresh(self, MLI):
        '''This function is the data gatherer'''
        while self.killEvent.wait(0):
            statusText = MLI.ml.recv_match(type="STATUSTEXT", blocking=True)     # Receive a status message
            self.log.info("Status Text Received: " + statusText.text)   # Write the message to the log

            if "LEAK" in statusText.text.upper():                       # If there is a leak,
                self.log.error("Leak detected: " + statusText.text)     # Record it in the log,
                MLI.leakAction(MLI.ml, MLI.sem)                         # Then run the appropriate response

            # Note the lack of a sleep statement here.
            # Waiting is done by the blocking mode of the recv_match function
        self.log.debug("Ending")
