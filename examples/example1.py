# Import interface
import mavlinkinterface
from pymavlink import mavutil
exit()
# Create interface object
MLI = mavlinkinterface.mavlinkInterface()

MLI.mavlinkConnection.arducopter_arm()

MLI.move("forward", 1, 100)

# Strafing square
MLI.move("forward", 5, 50)
MLI.move("left", 5, 100)
MLI.move("back", 5, 50)
MLI.move("right", 5, 100)

MLI.dive(1, -100)
MLI.dive(5, 100)
MLI.arm()
MLI.disarm()

MLI.mavlinkConnection.motors_armed()  # Looks broken

MLI.mavlinkConnection.set_mode("MANUAL")
MLI.mavlinkConnection.set_mode("ALT_HOLD")
MLI.mavlinkConnection.set_mode("STABILIZE")
MLI.mavlinkConnection.set_mode("ACRO")
# MLI.mavlinkConnection.set_mode("POSHOLD")
# MLI.mavlinkConnection.set_mode("AUTO")
# MLI.mavlinkConnection.set_mode("CIRCLE")
# MLI.mavlinkConnection.set_mode("GUIDED")

MLI.changeAltitude(1, -1)