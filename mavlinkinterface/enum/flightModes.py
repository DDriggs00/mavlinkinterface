from enum import Enum

class flightModes(Enum):
    manual = 'MANUAL'
    # Manual mode passes the pilot inputs directly to the motors, with no stabilization.
    # ArduSub always boots in Manual mode.
    stabilize = 'STABILIZE'
    # Stabilize mode is like Manual mode, with heading and attitude stabilization.
    depth_hold = 'ALT_HOLD'
    # Depth Hold is like Stabilize mode with the addition of depth stabilization
    # when the pilot throttle input is zero.
    # A depth sensor is required to use depth hold mode.
    position_hold = 'POSHOLD'  # REQUIRES GPS
    # Position Hold mode will stabilize the vehicle's absolute position, attitude,
    # and heading when the pilot control inputs are neutral.
    # The vehicle can be maneuvered and repositioned by the pilot.
    auto = 'AUTO'  # REQUIRES GPS
    # Auto mode executes the mission stored on the autopilot autonomously.
    # Pilot control inputs are ignored in most cases.
    # The vehicle may be disarmed, or the mode can be changed to abort the mission.
    circle = 'CIRCLE'  # REQUIRES GPS
    # Circle mode navigates in circles with the front of the vehicle facing the center point.
    guided = 'GUIDED'  # REQUIRES GPS
    # Guided mode allows the vehicle's target position to be set dynamically
    # by a ground control station or companion computer.
    # This allows 'Click to Navigate Here' interactions with a map.
    acro = 'ACRO'  # secret menu
    # Acro (Acrobatic) mode performs angular rate stabilization.
