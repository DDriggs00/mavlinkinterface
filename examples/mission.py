#!/usr/bin/env python3

# This example demonstrates the interaction between different execution modes

import mavlinkinterface     # Needed to use the library

# Create interface object, All calls will be made through this
# execMode="queue" means that the "queue" execution mode will be used when none is given to a function
mli = mavlinkinterface.mavlinkInterface(execMode="queue")

mli.arm()   # Enable the propellors.

# Create a mission, passing it the interface that will be used
myMission = mavlinkinterface.mission(mli)

# Add some waypoints to the mission
myMission.goToCoordinates(33.810561, -118.394265)
myMission.goToCoordinates(33.811006, -118.394265)
myMission.goToCoordinates(33.811006, -118.394749)
myMission.goToCoordinates(33.810561, -118.394749)
myMission.goToCoordinates(33.810561, -118.394265)

# Upload mission to Drone
myMission.upload()

# Start mission
myMission.start(True)

mli.setFlightMode('Stabilize')
