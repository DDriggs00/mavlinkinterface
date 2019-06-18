from pymavlink import mavutil
from mavlinkinterface.logger import getLogger

def arm(ml, sem):
    try:
        log = getLogger("Status")
        log.info("Sending arming signal")
        ml.mav.command_long_send(
            ml.target_system,
            ml.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,  # Confirmation
            1,  # param1: 1 = arm
            0,  # param2: Meaningless
            0,  # param3: Meaningless
            0,  # param4: Meaningless
            0,  # param5: Meaningless
            0,  # param6: Meaningless
            0)  # param7: Meaningless
    finally:
        sem.release()


def disarm(ml, sem):
    try:
        log = getLogger("Status")
        log.info("Sending disarming signal")
        ml.mav.command_long_send(
            ml.target_system,
            ml.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,  # Confirmation
            0,  # param1: 0 = disarm
            0,  # param2: Meaningless
            0,  # param3: Meaningless
            0,  # param4: Meaningless
            0,  # param5: Meaningless
            0,  # param6: Meaningless
            0)  # param7: Meaningless
    finally:
        sem.release()
