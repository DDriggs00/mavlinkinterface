from enum import Enum
# from threading import Semaphore

class MLFlightModes(Enum):
    manual = 0
    # Manual mode passes the pilot inputs directly to the motors, with no stabilization.
    # ArduSub always boots in Manual mode.
    stabilize = 1
    # Stabilize mode is like Manual mode, with heading and attitude stabilization.
    depth_hold = 2
    # Depth Hold is like Stabilize mode with the addition of depth stabilization
    # when the pilot throttle input is zero.
    # A depth sensor is required to use depth hold mode.
    position_hold = 3  # REQUIRES GPS
    # Position Hold mode will stabilize the vehicle's absolute position, attitude,
    # and heading when the pilot control inputs are neutral.
    # The vehicle can be maneuvered and repositioned by the pilot.
    auto = 4  # REQUIRES GPS
    # Auto mode executes the mission stored on the autopilot autonomously.
    # Pilot control inputs are ignored in most cases.
    # The vehicle may be disarmed, or the mode can be changed to abort the mission.
    circle = 5  # REQUIRES GPS
    # Circle mode navigates in circles with the front of the vehicle facing the center point.
    guided = 6  # REQUIRES GPS
    # Guided mode allows the vehicle's target position to be set dynamically
    # by a ground control station or companion computer.
    # This allows 'Click to Navigate Here' interactions with a map.
    acro = 7  # secret menu
    # Acro (Acrobatic) mode performs angular rate stabilization.


def setFlightMode(sem, mode):
    # set flight mode
    print("Setting Flight Mode to " + str(mode))
    sem.release()
    return
