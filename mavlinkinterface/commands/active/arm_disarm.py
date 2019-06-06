from pymavlink import mavutil
from threading import Semaphore     # For sem.release()

def arm(ml, sem):
    ml.mav.command_long_send(
        ml.target_system,
        ml.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,  # Confirmation
        1,  # 1 = arm
        0,  # Meaningless
        0,  # Meaningless
        0,  # Meaningless
        0,  # Meaningless
        0,  # Meaningless
        0)  # Meaningless

    sem.release()

def disarm(ml, sem):
    ml.mav.command_long_send(
        ml.target_system,
        ml.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,  # Confirmation
        0,  # 0 = disarm
        0,  # Meaningless
        0,  # Meaningless
        0,  # Meaningless
        0,  # Meaningless
        0,  # Meaningless
        0)  # Meaningless

    sem.release()
