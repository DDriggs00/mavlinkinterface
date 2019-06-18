#!/usr/bin/env python

import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.arm()

# Move away from the dock
MLI.move(0, 3, 100)

# Strafing square
MLI.move3d(50, 50, -50, 3)
MLI.move3d(50, -50, 50, 3)
MLI.setFlightMode("ALT_HOLD")
MLI.move(0, 3, 50)
MLI.move(270, 3, 100)
MLI.move(180, 3, 50)
MLI.move(90, 3, 100)
MLI.dive(1, 100)
