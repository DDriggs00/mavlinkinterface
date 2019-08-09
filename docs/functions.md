# Current Status

## Completed functions

These functions perform exactly as described in the readme

### Active

These functions cause the drone to take a physical action.  

- [arm()](active/arm.md)
- [disarm()](active/disarm.md)
- [setFlightMode( flightMode, execMode \<optional> )](active/setFlightMode.md)
- [move( direction, time, throttle \<optional>, absolute \<optional>, execMode \<optional> )](active/move.md)
- [move3d( throttleX, throttleY, throttleZ, time, execMode \<optional> )](active/move3d.md)
- [surface( execMode \<optional> )](active/surface.md)
- [setLights( brightness, execMode \<optional> )](active/lights.md)
- [gripperOpen( time, execMode \<optional> )](active/gripperOpen.md)
- [gripperClose( time, execMode \<optional> )](active/gripperClose.md)
- DEPRECATED: [wait( time, execMode \<optional> )](active/wait.md)

### Passive

These functions do not cause the drone to make any action other than reading a sensor

- [getDepth()](passive/getDepth.md)
- [getGyroscopeData()](passive/getGyroscopeData.md)
- [getAccelerometerData()](passive/getAccelerometerData.md)
- [getBatteryData()](passive/getBatteryData.md)
- [getHeading()](passive/getHeading.md)
- [getMagnetometerData()](passive/getMagnetometerData.md)
- [getPressureExternal()](passive/getPressureExternal.md)

### Configuration

These functions modify configuration values, which persist on the device between missions

- [setSurfacePressure( pressure \<optional> )](configuration/setSurfacePressure.md)
- [setFluidDensity( density \<optional> )](configuration/setFluidDensity.md)

### Utility

These functions do not fit into any of the other categories.

- [disableSensor( sensor, enable \<optional>)](utility/disableSensor.md)
- [log( message )](utility/log.md)
- [stopCurrentTask()](utility/stopCurrentTask.md)
- [stopAllTasks()](utility/stopAllTasks.md)
- [waitQueue()](utility/waitQueue.md)

## Mission Mode

Advanced functions relying on GPS fall under mission mode.  
See [here](missions.md) for more information on missions

## Partially completed functions

These functions work as described in the documentation, but to a lesser grade of accuracy. Details on the failings of each one included. These are actively under development

- [dive( depth, throttle \<optional>, absolute \<optional>, execMode \<optional> )](active/dive.md)
  - Rotates to the depth and stops thrusting, but may pass the depth on momentum
- [setLeakAction( action )](configuration/setLeakAction.md)
  - Currently the leak detection is implemented, but the return to base and custom script functions are not yet implemented.

## New Functions

These functions were not originally intended, but were added since the last update.  
After each update, these functions will be moved to the completed functions category.

- [getAltitude()](passive/getAltitude.md)
  - This takes advantage of the new sonar sensor
- [gps.getCoordinates()](passive/gps.getCoordinates.md)
  - This returns GPS Coordinates
- [mission commands](missions.md)
  - This allows the user to plan and execute missions
- [getTemperature()](passive/getTemperature.md)
  - This returns the temperature as read by the external pressure sensor
- [setDefaultExecMode( mode )](configuration/setDefaultExecMode.md)
  - This allows for the changing of the default execution mode after initialization
  - Note that this requires the queue to be empty and no commands to be executing.
- [getPressureInternal()](passive/getPressureInternal.md)
  - Returns the internal pressure as a float

## Modified Functions (complete)

These Functions were changed in a major way, which is explained below.  
After each update, these functions will be moved to the completed functions category.

- [yaw( degrees, absolute \<optional>, execMode \<optional> )](active/yaw.md)
  - Now has 3 stages:
    1. Until within 30 degrees of target, yaws at 50% power
    2. Until within 5 degrees of target, yaws at 25% power
    3. cancels rotational momentum by reversing thrust until rotation is stopped

## Not Started functions

- [cameraTilt( angle, speed \<optional>, absolute \<optional>, execMode \<optional> )](active/cameraTilt.md)
- [cameraStartFeed()](passive/cameraStartFeed.md)
- [cameraVideoStart( time \<optional>, resolution \<optional> )](passive/cameraVideoStart.md)
- [cameraVideoStop()](passive/cameraVideoStop.md)
- [cameraPhoto( resolution \<optional>, zoom \<optional>, )](passive/cameraPhoto.md)
- [getAllSensorData()](passive/getAllSensorData.md)
- [setLoggingLevel( level )](configuration/setLoggingLevel.md)
- [setRecordingInterval( sensor, interval )](configuration/setRecordingInterval.md)
- getSonarMap()
- All GPS-Related functions, including:
  - setGpsMode()
  - getCoordinates()
  - goToCoordinates()
  - setHome()
  - goToHome()
