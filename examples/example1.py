# Import interface
import mavlinkinterface
from pymavlink import mavutil

# Create interface object
MLI = mavlinkinterface.mavlinkInterface()

# Arm the drone
MLI.arm()

# Function test group 1
MLI.setLightsMax()
MLI.move(0, 3, 100)
MLI.dive(5, -100)
MLI.setFlightMode("ALT_HOLD")
MLI.diveDepth(10, absolute=False)
# Strafing square
MLI.move(0, 5, 50)
MLI.move(270, 5, 100)
MLI.move(180, 5, 50)
MLI.move(90, 5, 100)
MLI.yaw(90)

MLI.getDepth()
MLI.getPressureExternal()
MLI.dive(1, 100)
MLI.mavlinkConnection.motors_armed()  # Looks broken
MLI.mavlinkConnection.uptime

test = MLI.mavlinkConnection.recv_msg()
test.get_type()
test.get_fieldnames()
MLI.setFlightMode("MANUAL")
MLI.setFlightMode("ALT_HOLD")
MLI.setFlightMode("STABILIZE")


MLI.changeAltitude(1, -1)
test1 = MLI.mavlinkConnection.recv_msg()
test_pressure = MLI.mavlinkConnection.recv_match(type="SCALED_PRESSURE")
test_IMU = MLI.mavlinkConnection.recv_match(type="SCALED_IMU")
test_text = MLI.mavlinkConnection.recv_match(type="STATUSTEXT")
test_text.text.upper()

test2 = MLI.mavlinkConnection.recv_match(type="HEARTBEAT")
mavutil.mavlink.enums['MAV_TYPE'][test2.type].name
mavutil.mavlink.enums['MAV_AUTOPILOT'][test2.autopilot].name
mode = test2.base_mode
is128 = is64 = is32 = is16 = is8 = is4 = is2 = is1 = False
if mode >= 128:
    mode -= 128
    is128 = True
if mode >= 64:
    mode -= 64
    is64 = True
if mode >= 32:
    mode -= 32
    is32 = True
if mode >= 16:
    mode -= 16
    is16 = True
if mode >= 8:
    mode -= 8
    is8 = True
if mode >= 4:
    mode -= 4
    is4 = True
if mode >= 2:
    mode -= 2
    is2 = True
if mode >= 1:
    mode -= 1
    is1 = True
