# Startup steps
import mavlinkinterface                             # Import Interface
mli = mavlinkinterface.mavlinkInterface('queue')    # Create interface object
mli.arm()                                           # Arm the drone

# Test groups

# Test Group 0: set surface pressure
mli.setSurfacePressure()

# Test group 2: lights test
mli.setLights(100)
mli.wait(1)
mli.setLights(0)

# Test Group 3: surface and ALT_HOLD - Deep end
mli.move(0, 3)
mli.dive(-1.75)    # Deep end is 2m deep
mli.setFlightMode("ALT_HOLD")
mli.wait(15)
mli.setFlightMode("MANUAL")
mli.surface()

# Test group 4: Yaw
mli.yaw2(90)
mli.wait(3)
mli.yaw2(-90)
mli.wait(3)

# Finishing steps

mli.disarm()    # Disarm the drone
