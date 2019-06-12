import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.mavlinkConnection.arducopter_arm()

MLI.move("forward", 3, 100)

# Strafing square
MLI.mavlinkConnection.set_mode("ALT_HOLD")
MLI.dive(1, -100)
MLI.move("left", 3, 100)
MLI.move("right", 3, 100)
MLI.move("left", 3, 100)
MLI.move("right", 3, 100)
