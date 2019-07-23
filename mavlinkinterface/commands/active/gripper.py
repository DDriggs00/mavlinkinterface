from time import sleep  # for pressing button for a certain time


def gripperOpen(ml, sem, time):
    try:
        buttons = 1 << 10
        for i in range(int(time * 4)):
            ml.mav.manual_control_send(
                ml.target_system,
                0,          # x [ Range: -1000-1000; backward=-1000, forward=1000, 0 = No X-Axis thrust ]
                0,          # y [ Range: -1000-1000; Left=-1000, Right=1000, 0 = No Y-Axis thrust ]
                500,        # z [ Range: 0-1000; 0=down, 1000=up; 500 = no vertical thrust ]
                0,          # r [ Yaw, with counter-clockwise being negative. ]
                buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 == pressed]
            sleep(0.25)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,    # x [ Range: -1000-1000; backward=-1000, forward=1000, 0 = No X-Axis thrust ]
            0,    # y [ Range: -1000-1000; Left=-1000, Right=1000, 0 = No Y-Axis thrust ]
            500,  # z [ Range: 0-1000; 0=down, 1000=up; 500 = no vertical thrust ]
            0,    # r [ Yaw, with counter-clockwise being negative. ]
            0)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 == pressed]
    finally:
        sem.release()


def gripperClose(ml, sem, time):
    try:
        buttons = 1 << 9
        for i in range(int(time * 4)):
            ml.mav.manual_control_send(
                ml.target_system,
                0,          # x [ Range: -1000-1000; backward=-1000, forward=1000, 0 = No X-Axis thrust ]
                0,          # y [ Range: -1000-1000; Left=-1000, Right=1000, 0 = No Y-Axis thrust ]
                500,        # z [ Range: 0-1000; 0=down, 1000=up; 500 = no vertical thrust ]
                0,          # r [ Yaw, with counter-clockwise being negative. ]
                buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 == pressed]
            sleep(0.25)

        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,    # x [ Range: -1000-1000; backward=-1000, forward=1000, 0 = No X-Axis thrust ]
            0,    # y [ Range: -1000-1000; Left=-1000, Right=1000, 0 = No Y-Axis thrust ]
            500,  # z [ Range: 0-1000; 0=down, 1000=up; 500 = no vertical thrust ]
            0,    # r [ Yaw, with counter-clockwise being negative. ]
            0)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 == pressed]
    finally:
        sem.release()
