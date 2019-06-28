#!/usr/bin/env python3

import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.arm()

# MLI.move(0, 3, 100)

# Strafing square
MLI.dive(-1)
MLI.setFlightMode("ALT_HOLD")
MLI.move(0, 3, 50)
MLI.move(270, 3, 100)
MLI.move(180, 3, 50)
MLI.move(90, 3, 100)
MLI.surface()

input()
