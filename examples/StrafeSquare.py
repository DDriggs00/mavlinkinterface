import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.mavlinkConnection.arducopter_arm()

MLI.move("forward", 3, 100)

# Strafing square
MLI.move("forward", 3, 50)
MLI.move("left", 3, 100)
MLI.move("back", 3, 50)
MLI.move("right", 3, 100)
