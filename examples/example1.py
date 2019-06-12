# Import interface
import mavlinkinterface
from pymavlink import mavutil
# exit()
# Create interface object
MLI = mavlinkinterface.mavlinkInterface()

MLI.arm()

MLI.move("forward", 1, 100)

# Strafing square
MLI.move("forward", 5, 50)
MLI.move("left", 5, 100)
MLI.move("back", 5, 50)
MLI.move("right", 5, 100)
MLI.yaw2(90)

MLI.dive(10, -100)
MLI.dive(10, 100)
MLI.setLightsMax()
MLI.mavlinkConnection.motors_armed()  # Looks broken
MLI.mavlinkConnection.uptime
test = MLI.mavlinkConnection.recv_msg()
test.get_type()
test.time_boot_ms
test.get_header()
test.get_payload()
test.get_fieldnames()
test.onboard_control_sensors_enabled
test.onboard_control_sensors_present
test.voltage_battery
test.Vcc
test.Vservo
test.flags
MLI.setFlightMode("MANUAL")
MLI.setFlightMode("ALT_HOLD")
MLI.setFlightMode("STABILIZE")
MLI.setFlightMode("ACRO")
# MLI.mavlinkConnection.set_mode("POSHOLD")
# MLI.mavlinkConnection.set_mode("AUTO")
# MLI.mavlinkConnection.set_mode("CIRCLE")
# MLI.mavlinkConnection.set_mode("GUIDED")

MLI.changeAltitude(1, -1)
MLI.disarm()

test2 = MLI.mavlinkConnection.recv_match(type="SYS_STATUS")
test2.get_fieldnames()
test2.voltage_battery
test2.battery_remaining
test2.current_battery
test2.drop_rate_comm
test2.load

test2 = MLI.mavlinkConnection.recv_match(type="HEARTBEAT")
test2.get_fieldnames()
test2.type
test2.autopilot
test2.base_mode
test2.custom_mode
test2.system_status
test2.mavlink_version
mavutil.mavlink.enums['MAV_TYPE'][test2.type].name
mavutil.mavlink.enums['MAV_AUTOPILOT'][test2.autopilot].name
mavutil.mavlink.enums['MAV_MODE_FLAG'][test2.base_mode].name
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
i = 128

# def getAllData():

MLI.mavlinkConnection.set_servo(9, 1100)
