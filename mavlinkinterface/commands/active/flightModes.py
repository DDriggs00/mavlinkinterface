from pymavlink import mavutil

def setFlightMode(ml, sem, mode):
    # set flight mode
    try:
        print("Setting Flight Mode to " + str(mode))
        # if mode not in master.mode_mapping():
        #     print('Unknown mode : {}'.format(mode))
        #     print('Try:', list(master.mode_mapping().keys()))
        # exit(1)
        modeID = ml.mode_mapping()[mode]
        ml.mav.set_mode_send(
            ml.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            modeID)

    finally:
        sem.release()
