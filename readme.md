# Catfish API

## Features

- Python!
- Full Logging of some or all sensor data (configurable)
- All functions return either:
    1. a single variable
    2. A JSON-formatted string
- All physical commands have blocking, queueing, and regular modes, as well as  an override system
- Movement Commands can detect blockage
- All sensor info accessible individually or at once

Add modes
make surface override depth holding mode
"override" disables depth hold mode
add terrain-following mode once amanda makes one
heartbeat

## Architecture

- Written using Python 3.7 latest
- Dependencies
  - [pymavlink](https://github.com/ArduPilot/pymavlink)

## Active functions

TODO: add pitch, roll, setThrust, setAltitudeTarget

- [arm()](docs/Active/arm.md)
- [armGrab( strength \<optional>, percent \<optional> )](docs/Active/armGrab.md)
- [armRelease( percent \<optional> )](docs/Active/armRelease.md)
- [cameraTilt( angle, speed \<optional> )](docs/Active/cameraTilt.md)
- [disarm()](docs/Active/disarm.md)
- [dive( depth )](docs/Active/dive.md)
- [move( direction, time, throttle \<optional> )](docs/Active/move.md)
- [setFlightMode( mode )](docs/Active/setFlightMode.md)
- [setLights( brightness )](docs/Active/setLights.md)
- [surface()](docs/Active/surface.md)
- [yaw( degrees )](docs/Active/yaw.md)

## Passive functions

- [cameraStartFeed()](docs/Passive/cameraStartFeed.md)
- [cameraVideoStart( time \<optional>, resolution \<optional> )](docs/Passive/cameraVideoStart.md)
- [cameraVideoStop()](docs/Passive/cameraVideoStop.md)
- [cameraPhoto( resolution \<optional>, zoom \<optional>, )](docs/Passive/cameraPhoto.md)
- [getAccelerometerData()](docs/Passive/getAccelerometerData.md)
- [getBatteryData()](docs/Passive/getBatteryData.md)
- [getBearing()](docs/Passive/getBearing.md)
- [getDepth()](docs/Passive/getDepth.md)
- [getGyroscopeData()](docs/Passive/getGyroscopeData.md)
- [getLeakData()](docs/Passive/getLeakData.md)
- [getMagnetometerData()](docs/Passive/getMagnetometerData.md)
- [getPressureExternal()](docs/Passive/getPressureExternal.md)
- [getPressureInternal()](docs/Passive/getPressureInternal.md)
- [getTemperature()](docs/Passive/getTemperature.md)
- [getAllSensorData()](docs/Passive/getAllSensorData.md)

TODO:

- getSonarMap()

## Configuration functions

- [setLoggingLevel( sensor, level )](docs/Configuration/setLoggingLevel.md)
- [setRecordingInterval( interval )](docs/Configuration/setRecordingInterval.md)
- [setDefaultQueueMode( mode )](docs/Configuration/setDefaultQueueMode.md)

## Universal Parameters

### QueueMode (enum)  

This argument prevents all other active calls until the paired command has been finished or aborted.

- When override, any other action commands will override and stop the command.
- When queue, other action commands will be queued behind the command.
- When ignore, other action commands will be ignored until the command completes
- When this argument is not present, it will be treated as None (configurable)

### Override (switch)

When present, this argument causes any currently executing or queued commands to stop, and this command will to executed immediately.  This can also be used to force an arming of the propellers.

### Absolute (switch)

This argument causes movement commands to use absolute coordinates and directions, rather than coordinates and directions relative to the submarine.

- When present, direction is relative to magnetic north, depth is relative to the surface, etc.
- When absent, direction coordinates, depth, and distances are all relative to the submarine's current location and the direction it is facing

Note: This argument is only relevant where a direction, depth, or coordinates are present
