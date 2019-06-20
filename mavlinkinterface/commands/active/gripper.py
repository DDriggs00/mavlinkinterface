from time import sleep  # for pressing button for a certain time

def gripperOpen(ml, sem):
    try:
        buttons = 1 << 10
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.25)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            0)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        sem.release()

def gripperClose(ml, sem):
    try:
        buttons = 1 << 9
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            buttons)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
        sleep(0.25)
        # Reset button positions to zero
        ml.mav.manual_control_send(
            ml.target_system,
            0,          # x [ forward(1000)-backward(-1000)]
            0,          # y [ left(-1000)-right(1000) ]
            500,        # z [ maximum being 1000 and minimum being 0 on a joystick and the thrust of a vehicle.] "I suspect this code if for moving up and down
            0,          # r [ corresponds to a twisting of the joystick, with counter-clockwise being 1000 and clockwise being -1000, and the yaw of a vehicle]
            0)    # b [ A bitfield corresponding to the joystick buttons' current state, 1 for pressed, 0 for released. The lowest bit corresponds to Button 1]
    finally:
        sem.release()
