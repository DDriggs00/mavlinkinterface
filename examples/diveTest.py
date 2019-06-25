
import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.arm()

print(MLI.getDepth())
print(MLI.getPressureExternal())
MLI.dive(-0.5, 10)
MLI.setFlightMode("ALT_HOLD")

for i in range(5):
    MLI.wait(1)
    print(MLI.getDepth())
    print(MLI.getPressureExternal())

input()
