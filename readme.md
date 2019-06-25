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

- [arm()](docs/Active/arm.md)
- X [gripperClose( strength \<optional>, percent \<optional> )](docs/Active/armGrab.md)
- X [gripperOpen( percent \<optional> )](docs/Active/armRelease.md)
- X [cameraTilt( angle, speed \<optional> )](docs/Active/cameraTilt.md)
- [disarm()](docs/Active/disarm.md)
- [dive( depth, throttle \<optional> )](docs/Active/dive.md)
- [move( direction, time, throttle \<optional> )](docs/Active/move.md)
- [move3d( throttleX, throttleY, throttleZ, time )](docs/Active/move3d.md)
- [setFlightMode( mode )](docs/Active/setFlightMode.md)
- X [setLights( brightness )](docs/Active/setLights.md)
- [surface()](docs/Active/surface.md)
- B [yaw( degrees )](docs/Active/yaw.md)

## Passive functions

- X [cameraStartFeed()](docs/Passive/cameraStartFeed.md)
- X [cameraVideoStart( time \<optional>, resolution \<optional> )](docs/Passive/cameraVideoStart.md)
- X [cameraVideoStop()](docs/Passive/cameraVideoStop.md)
- X [cameraPhoto( resolution \<optional>, zoom \<optional>, )](docs/Passive/cameraPhoto.md)
- [getAccelerometerData()](docs/Passive/getAccelerometerData.md)
- [getBatteryData()](docs/Passive/getBatteryData.md)
- X [getHeading()](docs/Passive/getHeading.md)
- [getDepth()](docs/Passive/getDepth.md)
- [getGyroscopeData()](docs/Passive/getGyroscopeData.md)
- X [getLeakData()](docs/Passive/getLeakData.md)
- [getMagnetometerData()](docs/Passive/getMagnetometerData.md)
- [getPressureExternal()](docs/Passive/getPressureExternal.md)
- [getPressureInternal()](docs/Passive/getPressureInternal.md)
- X [getTemperature()](docs/Passive/getTemperature.md)
- X [getAllSensorData()](docs/Passive/getAllSensorData.md)

TODO:

- getSonarMap()

## Configuration functions

- X [setLoggingLevel( sensor, level )](docs/Configuration/setLoggingLevel.md)
- X [setRecordingInterval( interval )](docs/Configuration/setRecordingInterval.md)
- X [setDefaultQueueMode( mode )](docs/Configuration/setDefaultQueueMode.md)

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
