# Import interface
import mavlinkinterface

# Create interface object
MLI = mavlinkinterface.mavlinkInterface()


MLI.move("forward", 5, 50)

# Strafing square
MLI.move("forward", 5, 50)
MLI.move("left", 5, 100)
MLI.move("back", 5, 50)
MLI.move("right", 5, 100)

MLI.dive(5, -100)
MLI.dive(5, 100)