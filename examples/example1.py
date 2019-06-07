# Import interface
import mavlinkinterface
from pymavlink import mavutil
exit()
# Create interface object
MLI = mavlinkinterface.mavlinkInterface()


MLI.move("forward", 5, 50)

# Strafing square
MLI.move("forward", 5, 50)
MLI.move("left", 5, 100)
MLI.move("back", 5, 50)
MLI.move("right", 5, 100)

MLI.dive(5, -100)
MLI.dive(5, 100)
MLI.arm()
MLI.disarm()

MLI.mavlinkConnection.arducopter_arm()
MLI.mavlinkConnection.arducopter_disarm()
MLI.mavlinkConnection.motors_armed()  # Looks broken

MLI.mavlinkConnection.set_mode("MANUAL")
MLI.mavlinkConnection.set_mode("ALT_HOLD")
MLI.mavlinkConnection.set_mode("STABILIZE")
MLI.mavlinkConnection.set_mode("ACRO")

MLI.yawAbsolute(30, 20, 1, 0)
MLI.changeAltitude(1, -1)
# MLI.mavlinkConnection.set_mode("POSHOLD")
# MLI.mavlinkConnection.set_mode("AUTO")
# MLI.mavlinkConnection.set_mode("CIRCLE")
# MLI.mavlinkConnection.set_mode("GUIDED")

MLI.mavlinkConnection.mav.command_long_send(
    MLI.mavlinkConnection.target_system,
    MLI.mavlinkConnection.target_component,
    mavutil.mavlink.ATTITUDE,
    0,  # Confirmation
    1,  # param1: 1 = arm
    0,  # param2: Meaningless
    0,  # param3: Meaningless
    0,  # param4: Meaningless
    0,  # param5: Meaningless
    0,  # param6: Meaningless
    0)  # param7: Meaningless
