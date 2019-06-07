from pymavlink import mavutil

def setFlightMode(ml, sem, mode):
    # set flight mode
    try:
        mode = "Depth Hold"
        mode = mode.upper()
        print("Setting Flight Mode to " + str(mode))
        if mode in ("MANUAL", "CIRCLE", "GUIDED", "ACRO"):
            pass
        elif "DEPTH" in mode and "HOLD" in mode:
            mode = "ALT_HOLD"
        elif "STABIL" in mode:
            mode = "STABILIZE"
        elif "POSITION" in mode:
            mode = "POS_HOLD"

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
