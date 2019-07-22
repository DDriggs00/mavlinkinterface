# Catfish API

## Features

- Full Logging of some or all sensor data (configurable)
- All returning functions return either:
    1. a single variable, or
    2. A JSON-formatted string
- [Multiple methods for handling sequential commands](docs/executionModes.md)
- All sensor info accessible
  - Per sensor
  - Per sensor module (eg. IMU, SENSOR_POD_1)
  - Together
- Easily switch between flight modes

## TODO

make surface override depth holding mode
"override" disables depth hold mode
add terrain-following mode once amanda makes one
heartbeat

## Installation

1. Install python 3 (See instructions [here](https://realpython.com/installing-python/))
   - If ppi3 was not installed along with python, install it now
1. Install pymavlink
   - `pip3 install pymavlink` Note: Use the `--user` flag on Windows
1. Install bluerobotics-ping
   - `pip3 install bluerobotics-ping` Note: Use the `--user` flag on Windows
1. Download this repository
1. Navigate a terminal or administrator CMD prompt to the folder containing `setup.py`
1. Run `python3 ./setup.py install`

## Usage

To use this library, you must already have an underwater drone set up and working with qGroundControl.  Once that is working, perform the following steps.

1. Import the library in your python script
   - `import mavlinkinterface`
1. Create an instance of the interface. All interactions with the drone will be completed through this interface. Note that you may provide a default execution mode (see [here](docs/executionModes.md) for details)
   - `MLI = mavlinkinterface.mavlinkInterface(execMode="queue")`
1. If you are diving for the first time in a given body of water, set the surface pressure.
   - [`MLI.setSurfacePressure()`](docs/configuration/setSurfacePressure.md)
1. If you are diving in a medium that has a different density from fresh water or the last used medium (eg. salt water), set the density
   - [`MLI.setFluidDensity(1027)`](docs/configuration/setFluidDensity.md)
1. Arm the Drone
   - [`MLI.arm()`](docs/active/arm.md)
1. Proceed with script
1. Disarm the Drone
   - [`MLI.disarm()`](docs/active/disarm.md)

See [the examples](examples/) for more in-depth instructions.

## Function List

For Full function list, see [here](docs/functions.md)

## Common Parameters

### execMode (string)  

This sets the execution mode of the attached command. For information of the various execution modes, see [here](docs/executionModes.md)

### Absolute (switch)

This argument causes movement commands to use absolute coordinates and directions, rather than coordinates and directions relative to the drone.

- When present, direction is relative to magnetic north, depth is relative to the surface, etc.
- When absent, direction coordinates, depth, and distances are all relative to the drone's current location and the direction it is facing

Note: This argument is only relevant where a direction, depth, or coordinates are present
