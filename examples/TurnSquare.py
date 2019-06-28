#!/usr/bin/env python3

import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.arm()

MLI.move(0, 3, 100)

# Strafing square
MLI.move(0, 3, 50)
MLI.yaw(90)
MLI.move(0, 3, 50)
MLI.yaw(90)
MLI.move(0, 3, 50)
MLI.yaw(90)
MLI.move(0, 3, 50)
MLI.yaw(90)
