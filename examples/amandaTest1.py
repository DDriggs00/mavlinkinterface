###############################################################################
#
# Amanda Ward
# This is code to test Devin Driggs's API
###############################################################################

import mavlinkinterface
import time
MLI = mavlinkinterface.mavlinkInterface('queue')
MLI.arm()


# the light test worked :)
def testLights():
    MLI.setLights(50, execMode='synchronous')
    # Turns the lights off
    time.sleep(7)
    MLI.setLights(100, execMode='synchronous')
    # sets the lights to 65% brightness
    time.sleep(7)
    MLI.setLights(brightness=0, execMode='synchronous')
    # sets the lights to full brightness
    time.sleep(10)
    MLI.setLights(brightness=100, execMode='synchronous')


# the light test worked :)
def gradualLightUp():
    MLI.setLights(0)
    # Turns the lights off
    time.sleep(3)
    MLI.setLights(10)
    # sets the lights to 65% brightness
    time.sleep(3)
    MLI.setLights(brightness=20)
    # sets the lights to full brightness
    time.sleep(3)
    MLI.setLights(brightness=30)
    time.sleep(3)
    MLI.setLights(brightness=40)
    time.sleep(3)
    MLI.setLights(brightness=50)
    time.sleep(3)
    MLI.setLights(brightness=60)
    time.sleep(3)
    MLI.setLights(brightness=70)
    time.sleep(3)
    MLI.setLights(brightness=80)
    time.sleep(3)
    MLI.setLights(brightness=90)
    time.sleep(3)
    MLI.setLights(brightness=100)


# the light test worked :)
def gradualLightDown():
    MLI.setLights(100)
    # Turns the lights off
    time.sleep(3)
    MLI.setLights(90)
    # sets the lights to 65% brightness
    time.sleep(3)
    MLI.setLights(brightness=80)
    # sets the lights to full brightness
    time.sleep(3)
    MLI.setLights(brightness=70)
    time.sleep(3)
    MLI.setLights(brightness=60)
    time.sleep(3)
    MLI.setLights(brightness=50)
    time.sleep(3)
    MLI.setLights(brightness=40)
    time.sleep(3)
    MLI.setLights(brightness=30)
    time.sleep(3)
    MLI.setLights(brightness=20)
    time.sleep(3)
    MLI.setLights(brightness=10)
    time.sleep(3)
    MLI.setLights(brightness=0)


# I tested the gripper functions and they do not work
def gripperOpen():
    MLI.gripperOpen(1)
    # not sure how long to make gripper open!


def gripperClose():
    MLI.gripperClose(1)
    # The grabber arm closes for 1/2 second


# gradualLightDown()
# gradualLightUp()

gripperOpen()
# gripperClose()
