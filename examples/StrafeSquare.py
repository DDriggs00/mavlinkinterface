import mavlinkinterface
MLI = mavlinkinterface.mavlinkInterface()
MLI.arm()

MLI.move("forward", 3, 100)

# Strafing square
MLI.dive(1, -100)
MLI.move("forward", 3, 50)
MLI.move("left", 3, 100)
MLI.move("back", 3, 50)
MLI.move("right", 3, 100)
MLI.dive(1, 100)
