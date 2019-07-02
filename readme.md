# Catfish API

## Features

- Full Logging of some or all sensor data (configurable)
- All returning functions return either:
    1. a single variable, or
    2. A JSON-formatted string
- [Multiple methods for handling sequential commands](docs/executionModes.md)
- All sensor info accessible
  - Per sensor
  - Per sensor module
  - Together
- Easily switch between flight modes

## TODO

make surface override depth holding mode
"override" disables depth hold mode
add terrain-following mode once amanda makes one
heartbeat

## Installation

1. Install python 3 (See instructions [here](https://realpython.com/installing-python/))
1. Install pymavlink (See instructions [here](https://github.com/ArduPilot/pymavlink))
1. Download this repository
1. Navigate a shell or administrator CMD prompt to the folder containing `setup.py`
1. Run `python3 ./setup.py install`

## Usage

To use this library, you must already have an underwater drone set up and working with qGroundControl.  Once that is working, see [the examples](examples/).

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
