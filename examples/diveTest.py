
import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
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

input()
