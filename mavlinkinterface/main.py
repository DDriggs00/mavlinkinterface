# Regular Imports
from threading import Thread        # For pretty much everything
from threading import Semaphore     # For keeping only one thread running
from enum import Enum               # For QueueModes
from time import sleep              # For heartbeat
from datetime import datetime       # For naming log file
import logging                      # For logging

# Local Imports
import mavlinkinterface.commands as commands


class QueueModes(Enum):
    queue = 0
    override = 1
    ignore = 2


class mavlinkInterface(object):
    def __init__(self, queueMode=QueueModes.override, asynchronous=False):
        # Set up Logging
        logFileName = 'log_' + str(datetime.now()) + '.log'
        logging.basicConfig(filename=logFileName,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
        # Set class variables
        self.queueMode = queueMode
        self.asynchronous = asynchronous
        self.lightBrightness = 0
        self.flightMode = commands.active.MLFlightModes.manual
        self.s = Semaphore(1)
        logging.debug("Starting Heartbeat")
        heartbeat.enabled = True
        self.hb = Thread(target=heartbeat)
        self.hb.start()
        # self.hb.join()
        logging.debug("Interface successfully started")

    def stopAll(self):
        heartbeat.enabled = False
        if self.queueMode == QueueModes.queue:
            # Clear queue
            pass
        self.stopCurrent()

    def stopCurrent(self):
        # Kills the currently running task and stops the submarine
        pass

    def setLights(self, brightness):
        self.lightBrightness = brightness
        t = Thread(target=commands.active.setLights, args=(brightness,))
        t.start()
        if(not self.asynchronous):
            t.join()

    def setFlightMode(self, mode, override=False):
        # logging.debug("self.s._value")
        logging.debug(self.s._value)
        if self.s.acquire(blocking=False):
            pass
        else:
            if self.queueMode == QueueModes.ignore:
                print("Using Ignore mode, this command will now be discarded")
                return
            elif self.queueMode == QueueModes.override or override:
                logging.info("Override active, Killing existing task")
                # Kill existing task
                logging.info("Force-Releasing Semaphore")
                self.s.release()
                # Now that previous action has been killed, execute current action
        logging.info("Setting flight mode")
        self.flightMode = mode
        t = Thread(target=commands.active.setFlightMode, args=(self.s, mode,))
        t.start()
        if(not self.asynchronous):
            t.join()
        logging.debug("self.s._value after function")
        logging.debug(self.s._value)


def heartbeat():
    while heartbeat.enabled:
        logging.info("beat")
        sleep(15)

# def queueManager(q, sem):
#     while True:
#         t = q.get(block=True)
