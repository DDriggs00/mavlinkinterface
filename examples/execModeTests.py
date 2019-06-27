
import mavlinkinterface     # Needed to use the library

# Create interface object, All calls will be made through this
# execMode="queue" means that the "queue" execution mode will be used when none is given to a function
MLI = mavlinkinterface.mavlinkInterface(execMode="queue")

MLI.arm()   # Enable the propellors

MLI.move(90, 3)     # Strafe right for 3 sec
MLI.move(270, 3)    # Move left for 3 sec


MLI.move(0, 3, execMode="override")      # Move forward for 3 sec
