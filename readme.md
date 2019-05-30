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
add pitch, roll, setThrust, setAltitudeTarget

- [yaw( degrees )](docs/Active/yaw.md)
- [move( direction, time, throttle \<optional> )](docs/Active/move.md)
- [dive( depth )](docs/Active/dive.md)
- [surface()](docs/Active/surface.md)
- [armGrab( strength \<optional>, percent \<optional> )](docs/Active/armGrab.md)
- [armRelease( percent \<optional> )](docs/Active/armRelease.md)
- [lights( brightness )](docs/Active/lights.md)
- [cameraTilt( angle, speed <optional> )](docs/Active/cameraTilt.md)
- [arm()](docs/Active/arm.md)
- [disarm()](docs/Active/disarm.md)

## Passive functions
- [cameraStartFeed()](docs/Passive/cameraStartFeed.md)
- [cameraVideoStart( time \<optional>, resolution \<optional> )](docs/Passive/cameraVideoStart.md)
- [cameraVideoStop()](docs/Passive/cameraVideoStop.md)
- [cameraPhoto( resolution \<optional>, zoom \<optional>, )](docs/Passive/cameraPhoto.md)
- [getLeakData()](docs/Passive/getLeakData.md)
- [getDepth()](docs/Passive/getDepth.md)
- [getPressureExternal()](docs/Passive/getPressureExternal.md)
- [getPressureInternal()](docs/Passive/getPressureInternal.md)
- [getTemperature()](docs/Passive/getTemperature.md)
- [getBearing()](docs/Passive/getBearing.md)
- [getBatteryData()](docs/Passive/getBatteryData.md)
- [getMagnetometerData()](docs/Passive/getMagnetometerData.md)
- [getAccelerometerData()](docs/Passive/getAccelerometerData.md)
- [getGyroscopeData()](docs/Passive/getGyroscopeData.md)

TODO:

- getSonarMap()
# getAllSensorData()
Returns data from all sensors

## Return Values
Returns a JSON-formatted string.  
Returns all data from every currently-attached sensor
## Example Output


- getAllPassiveSensorData()

## Configuration functions

- [setLoggingLevel( sensor, level )](docs/Configuration/setLoggingLevel.md)
- [setRecordingInterval( interval )](docs/Configuration/setRecordingInterval.md)

TODO:
# setDefaultQueueMode( mode )
Sets the queuing mode to use when the universal parameter queueMode is not given.
The possible modes are as follows:

Queue mode:
> If a movement command is currently executing and a new move command is initiated, the new move command will be placed in a queue, which will be executed immediately following the existing command.

Override mode:
> If a movement command is currently executing and a new move command is initiated, the currently executing movement command will be halted and discarded, and the new command will be executed immediately. The *Override* causes any command to behave as though this mode were active.

Ignore mode:
> If a movement command is currently executing and a new move command is initiated, the new move command will be ignored.

The default default mode is override

## Parameters
Mode (enum):  
> The queuing mode to use by default. Possible values are:  
> queue  
> override  
> ignore



## Universal Parameters

### QueueMode (enum)  
This argument prevents all other active calls until the paired command has been finished or aborted.  
* When override, any other action commands will override and stop the command.  
* When queue, other action commands will be queued behind the command.  
* When ignore, other action commands will be ignored until the command completes  
* When this argument is not present, it will be treated as None (configurable)

### Override (switch)
When present, this argument causes any currently executing or queued commands to stop, and this command will to executed immediately.  This can also be used to force an arming of the propellers.

### Absolute (switch)
This argument causes movement commands to use absolute coordinates and directions, rather than coordinates and directions relative to the submarine.
* When present, direction is relative to magnetic north, depth is relative to the surface, etc.
* When absent, direction coordinates, depth, and distances are all relative to the submarine's current location and the direction it is facing

Note: This argument is only relevant where a direction, depth, or coordinates are present
