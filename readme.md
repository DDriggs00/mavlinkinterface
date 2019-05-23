# Catfish API

## Features

- Python!
- Full Logging of some or all sensor data (configurable)
- All functions return either:
    1. a single variable
    1. A JSON string
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
add pitch, roll, setThrust, setAltitudeTarget

- [yaw( degrees )](Documentation/Active/yaw.md)
- [move( direction, time, throttle \<optional> )](Documentation/Active/move.md)
- [dive( depth )](Documentation/Active/dive.md)
- [surface()](Documentation/Active/surface.md)
- [armGrab( strength \<optional>, percent \<optional> )](Documentation/Active/armGrab.md)
- [armRelease( percent \<optional> )](Documentation/Active/armRelease.md)
- [lights( brightness )](Documentation/Active/lights.md)
- [cameraTilt( angle, speed <optional> )](Documentation/Active/cameraTilt.md)
- [arm()](Documentation/Active/arm.md)
- [disarm()](Documentation/Active/disarm.md)

## Passive functions
- [cameraStartFeed()](Documentation/Passive/cameraStartFeed.md)
- [cameraVideoStart( time \<optional>, resolution \<optional> )](Documentation/Passive/cameraVideoStart.md)
- [cameraVideoStop()](Documentation/Passive/cameraVideoStop.md)
- [cameraPhoto( resolution \<optional>, zoom \<optional>, )](Documentation/Passive/cameraPhoto.md)
- [getLeakData()](Documentation/Passive/getLeakData.md)
- [getDepth()](Documentation/Passive/getDepth.md)
- [getPressureExternal()](Documentation/Passive/getPressureExternal.md)
- [getPressureInternal()](Documentation/Passive/getPressureInternal.md)
- [GetTemperature()](Documentation/Passive/getTemperature.md)
- [getBearing()](Documentation/Passive/getBearing.md)
- [GetBatteryData()](Documentation/Passive/getBatteryData.md)

TODO:
- getAccelerometerData()
- getGyroscopeData()
- getSonarMap
- getAllSensorData
- getAllPassiveSensorData

## Configuration functions

- [setLoggingLevel( sensor, level )](Documentation/Configuration/setLoggingLevel.md)
- [setRecordingInterval( interval )](Documentation/Configuration/setRecordingInterval.md)

TODO:
- setDefaultBlockMode()

## Universal Parameters

### BlockMode (enum)  
This argument prevents all other active calls until the paired command has been finished or aborted.  
* When None, any other action commands will override and stop the command.  
* When Queue, other action commands will be queued behind the command.  
* When Block, other action commands will be ignored until the command completes  
* When this argument is not present, it will be treated as None (configurable)

### Override (switch)
When present, this argument causes any currently executing or queued commands to stop, and this command will to executed immediately.  This can also be used to force an arming of the propellers.

### Absolute (switch)
This argument causes movement commands to use absolute coordinates and directions, rather than coordinates and directions relative to the submarine.
* When present, direction is relative to magnetic north, depth is relative to the surface, etc.
* When absent, direction coordinates, depth, and distances are all relative to the submarine's current location and the direction it is facing

Note: This argument is only relevant where a direction, depth, or coordinates are present
