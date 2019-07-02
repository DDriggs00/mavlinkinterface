#!/usr/bin/env python3

# This example demonstrates the interaction between different execution modes

import mavlinkinterface     # Needed to use the library
from time import sleep      # For waiting between commands

# Create interface object, All calls will be made through this
# execMode="queue" means that the "queue" execution mode will be used when none is given to a function
MLI = mavlinkinterface.mavlinkInterface(execMode="queue")

MLI.arm()   # Enable the propellors.

MLI.move(0, 1, execMode="synchronous")
print("synchronous command has ended")

# MLI.setFlightMode("STABILIZE")  # Sets the sub to stabilize itself. For more info, see docs/

# Add some commands to the queue
MLI.move(90, 3)     # Strafe right for 3 sec, Since no execMode flag is given, reverts to queue (see above)
MLI.move(270, 3)    # Strafe left  for 3 sec, Since no execMode flag is given, reverts to queue (see above)
MLI.move(90, 3)     # Strafe right for 3 sec, Since no execMode flag is given, reverts to queue (see above)
MLI.move(270, 3)    # Strafe left  for 3 sec, Since no execMode flag is given, reverts to queue (see above)
MLI.move(90, 3)     # Strafe right for 3 sec, Since no execMode flag is given, reverts to queue (see above)
MLI.move(270, 3)    # Strafe left  for 3 sec, Since no execMode flag is given, reverts to queue (see above)
print("all queuing commands have been added to the queue")
# Wait 5 seconds to give the queue a chance to start
sleep(5)

MLI.move(0, 5, execMode="override")      # Move forward for 5 sec
MLI.move(180, 3, execMode="synchronous")    # Move backward for 3 sec
