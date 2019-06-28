#!/usr/bin/env python3

import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.arm()

MLI.move(0, 3, 100)

# Strafing square
MLI.dive(-1)
MLI.setFlightMode("ALT_HOLD")
MLI.wait(10)
MLI.setFlightMode("STABILIZE")
MLI.move(0, 5, 10)
MLI.setFlightMode("MANUAL")
MLI.move(180, 5, 10)
MLI.surface()
