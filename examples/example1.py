# Startup steps
from time import sleep
import mavlinkinterface                             # Import Interface

mli = mavlinkinterface.mavlinkInterface('queue')    # Create interface object
# mli = mavlinkinterface.mavlinkInterface('queue', sitl=True)    # Create interface object

mli.arm()                                           # Arm the drone

# Test Group 0: set surface pressure
mli.setSurfacePressure()


# mli.setFlightMode('MANUAL')
# mli.setFlightMode('STABILIZE')
mli.setFlightMode('ALT_HOLD')

mli.move(0, 5, execMode='synchronous')
mli.dive(-1, 25, execMode='synchronous')
sleep(5)
mli.surface()


mli.move(180, 5, execMode='synchronous')


mli.move3d(0, 0, 100, 3)

sleep(10)

pass
# Test group 2: lights test
# mli.setLights(100)
# mli.wait(1)
# mli.setLights(0)


# # Test Group 3: surface and ALT_HOLD - Deep end
# f = open()
# mli.dive(-1)    # Deep end is 2m deep
# mli.setFlightMode("ALT_HOLD")
# mli.wait(15)
# mli.setFlightMode("MANUAL")
# mli.surface()

# # Test group 4: Yaw
mli.yaw(90)
# mli.wait(3)
# mli.yaw2(-90)
# mli.wait(3)

# # Finishing steps

# mli.disarm()    # Disarm the drone
