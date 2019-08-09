#!/usr/bin/env python3

import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface(execMode='synchronous')
MLI.arm()

MLI.move(0, 3)

print(MLI.getDepth())
print(MLI.getPressureExternal())
MLI.dive(-1, 50)
MLI.setFlightMode("alt_hold")

for i in range(5):
    MLI.wait(2)
    print(MLI.getDepth())
    print(MLI.getPressureExternal())

MLI.surface()

input()     # Keep window open until pressing return
