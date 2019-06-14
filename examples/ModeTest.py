#!/usr/bin/env python

import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.arm()

MLI.move(0, 3, 100)

# Strafing square
MLI.dive(1, -100)
MLI.mavlinkConnection.set_mode("ALT_HOLD")
MLI.move(270, 3, 100)
MLI.move(90, 3, 100)
MLI.move(270, 3, 100)
MLI.move(90, 3, 100)
