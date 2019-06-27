# Catfish API

## Features

- Written in Python 3
- Full Logging of some or all sensor data (configurable)
- All returning functions return either:
    1. a single variable, or
    2. A JSON-formatted string
- Multiple methods for handling sequential commands
  - Synchronous: Action commands will return only when completed.
  - Override: Any newer action commands will override and prior commands.
  - Queue: Any newer action commands will be added to a queue behind existing commands.
  - Ignore: Any newer action commands will be ignored if another action command is executing
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

## Architecture

- Written using Python 3.7 latest
- Dependencies
  - [pymavlink](https://github.com/ArduPilot/pymavlink)
  - pyquaternian

## Active functions

TODO: add pitch, roll, setThrust, setAltitudeTarget

X: Item is not yet Implemented  
B: A Basic version has been Implemented

- [arm()](docs/active/arm.md)
- X [gripperClose( strength \<optional>, percent \<optional> )](docs/active/armGrab.md)
- X [gripperOpen( percent \<optional> )](docs/active/armRelease.md)
- X [cameraTilt( angle, speed \<optional> )](docs/active/cameraTilt.md)
- [disarm()](docs/active/disarm.md)
- [dive( depth, throttle \<optional> )](docs/active/dive.md)
- [move( direction, time, throttle \<optional> )](docs/active/move.md)
- [move3d( throttleX, throttleY, throttleZ, time )](docs/active/move3d.md)
- [setFlightMode( mode )](docs/active/setFlightMode.md)
- X [setLights( brightness )](docs/active/setLights.md)
- [surface()](docs/active/surface.md)
- B [yaw( degrees )](docs/active/yaw.md)

## Passive functions

- X [cameraStartFeed()](docs/passive/cameraStartFeed.md)
- X [cameraVideoStart( time \<optional>, resolution \<optional> )](docs/passive/cameraVideoStart.md)
- X [cameraVideoStop()](docs/passive/cameraVideoStop.md)
- X [cameraPhoto( resolution \<optional>, zoom \<optional>, )](docs/passive/cameraPhoto.md)
- [getAccelerometerData()](docs/passive/getAccelerometerData.md)
- [getBatteryData()](docs/passive/getBatteryData.md)
- X [getHeading()](docs/passive/getHeading.md)
- [getDepth()](docs/passive/getDepth.md)
- [getGyroscopeData()](docs/passive/getGyroscopeData.md)
- X [getLeakData()](docs/passive/getLeakData.md)
- [getMagnetometerData()](docs/passive/getMagnetometerData.md)
- [getPressureExternal()](docs/passive/getPressureExternal.md)
- [getPressureInternal()](docs/passive/getPressureInternal.md)
- X [getTemperature()](docs/passive/getTemperature.md)
- X [getAllSensorData()](docs/passive/getAllSensorData.md)

TODO:

- getSonarMap()

## Configuration functions

- X [setLoggingLevel( sensor, level )](docs/configuration/setLoggingLevel.md)
- X [setRecordingInterval( interval )](docs/configuration/setRecordingInterval.md)
- X [setDefaultQueueMode( mode )](docs/configuration/setDefaultQueueMode.md)

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

This argument causes movement commands to use absolute coordinates and directions, rather than coordinates and directions relative to the drone.

- When present, direction is relative to magnetic north, depth is relative to the surface, etc.
- When absent, direction coordinates, depth, and distances are all relative to the drone's current location and the direction it is facing

Note: This argument is only relevant where a direction, depth, or coordinates are present
