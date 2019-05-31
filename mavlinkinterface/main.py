# Regular Imports
from threading import Thread
from enum import Enum

# Local Imports
import mavlinkinterface.commands.active


class queueModes(Enum):
    queue = 0
    override = 1
    ignore = 2


class mavlinkInterface:
    def __Init__(self, queueMode="Override", asynchronous=False):
        # Constructor
        print("Interface successfully started")

    def setLights(brightness):
        t = Thread(target=Commands.Active.lights.setLights, args=(100))
        t.start()
