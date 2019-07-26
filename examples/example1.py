# Startup steps
from time import sleep
import mavlinkinterface                             # Import Interface
from datetime import datetime

mli = mavlinkinterface.mavlinkInterface('queue')    # Create interface object
# mli = mavlinkinterface.mavlinkInterface('queue', sitl=True)    # Create interface object
mli.arm()                                           # Arm the drone

# Test Group 0: set surface pressure
mli.setSurfacePressure()
mli.setFlightMode('STABILIZE')

for i in range(3):
    mli.move(0, 5, execMode='synchronous')
    mli.move3d(0, 0, 100, 10)
    sleep(7)
    # coords = mli.gps.getCoordinates()
    mli.dive(-1, 15, execMode='synchronous')
    mli.setFlightMode('ALT_HOLD')
    for j in range(4):
        with open('/home/csstudent/logs/testlog.log', 'a+') as f:
            mli.dive(-1, 25, execMode='synchronous')
            f.write(str(datetime.now()))
            # f.write(coords)
            # f.write(mli.getAltitude())
            f.write(str(mli.getDepth()))
            sleep(1)
    mli.surface()
pass
# Test group 2: lights test
# mli.setLights(100)
# mli.wait(1)
# mli.setLights(0)


# Test Group 3: surface and ALT_HOLD - Deep end
f = open()
mli.dive(-1)    # Deep end is 2m deep
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
