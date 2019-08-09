#!/usr/bin/env python3

import mavlinkinterface
from time import sleep

MLI = mavlinkinterface.mavlinkInterface(execMode='synchronous')
MLI.arm()

MLI.move(0, 3, 100)

# Strafing square
MLI.dive(-1)
MLI.setFlightMode("ALT_HOLD")
sleep(10)
MLI.setFlightMode("STABILIZE")
MLI.move(0, 5, 10)
MLI.setFlightMode("MANUAL")
MLI.move(180, 5, 10)
MLI.surface()
