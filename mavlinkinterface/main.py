# Regular Imports
from threading import Thread
from enum import Enum

# Local Imports
import mavlinkinterface.commands as commands


class MLIQueueModes(Enum):
    queue = 0
    override = 1
    ignore = 2


class mavlinkInterface:
    def __Init__(self, queueMode=MLIQueueModes.override, asynchronous=False):
        # Constructor
        print("Interface successfully started")

    def setLights2(self, brightness):
        t1 = Thread(target=commands.active.setLights, args=(brightness,))
        t1.start()
        t1.join()
