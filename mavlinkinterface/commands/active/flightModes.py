# from pymavlink import mavutil

def setFlightMode(ml, sem, mode):
    # set flight mode
    try:
        # mode = "Depth Hold"
        mode = mode.upper()
        if mode in ("MANUAL", "CIRCLE", "GUIDED", "ACRO", "ALT_HOLD", "POS_HOLD", "STABILIZE"):
            pass
        elif "DEPTH" in mode and "HOLD" in mode:
            mode = "ALT_HOLD"
        elif "STABIL" in mode:
            mode = "STABILIZE"
        elif "POSITION" in mode:
            mode = "POS_HOLD"
        else:
            print("Sorry, that mode does not exist. Valid flight modes are: MANUAL, CIRCLE, GUIDED, ACRO, ALT_HOLD, POS_HOLD, STABILIZE")
            return
        print("Setting Flight Mode to " + str(mode))

        ml.set_mode(mode)

    finally:
        sem.release()
