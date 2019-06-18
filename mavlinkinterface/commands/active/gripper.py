from pymavlink import mavutil

def openGripper(ml, sem):
    try:
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

# MAV_CMD_DO_GRIPPER
