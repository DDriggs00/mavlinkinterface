# from pymavlink import mavutil

def setFlightMode(ml, sem, mode):
    # set flight mode
    try:
        # mode = "Depth Hold"
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

        ml.set_mode(mode)

    finally:
        sem.release()
