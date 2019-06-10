import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.mavlinkConnection.arducopter_arm()

MLI.move("forward", 3, 100)

# Strafing square
MLI.move("forward", 3, 50)
MLI.yaw(90)
MLI.move("forward", 3, 50)
MLI.yaw(90)
MLI.move("forward", 3, 50)
MLI.yaw(90)
MLI.move("forward", 3, 50)
MLI.yaw(90)
