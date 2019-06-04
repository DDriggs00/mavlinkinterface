# Import all functions
from mavlinkinterface.commands.active.lights import setLights
from mavlinkinterface.commands.active.flightModes import setFlightMode
from mavlinkinterface.commands.active.flightModes import MLFlightModes

# For importing all at once
__all__ = ["setLights", "setFlightMode", "MLFlightModes"]
