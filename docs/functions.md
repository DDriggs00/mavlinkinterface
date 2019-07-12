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

## Partially completed functions

These functions work as described in the documentation, but to a lesser grade of accuracy. Details on the failings of each one included. These are actively under development

- [dive( depth, throttle \<optional>, absolute \<optional>, execMode \<optional> )](active/dive.md)
- [yaw( degrees, absolute \<optional>, execMode \<optional> )](active/yaw.md)
- [setLeakAction( action )](configuration/setLeakAction.md)

## New Functions

These functions were not originally intended, but were added since the last update.  
After each update, these functions will be moved to the completed functions category.

- [getAltitude()](passive/getAltitude.md)
  - This takes advantage of the new sonar sensor

## Modified Functions (complete)

These Functions were changed in a major way, which is explained below.  
After each update, these functions will be moved to the completed functions category.

- No new notable changes

## Not Started functions

- [cameraTilt( angle, speed \<optional>, absolute \<optional>, execMode \<optional> )](active/cameraTilt.md)
- [cameraStartFeed()](passive/cameraStartFeed.md)
- [cameraVideoStart( time \<optional>, resolution \<optional> )](passive/cameraVideoStart.md)
- [cameraVideoStop()](passive/cameraVideoStop.md)
- [cameraPhoto( resolution \<optional>, zoom \<optional>, )](passive/cameraPhoto.md)
- [getPressureInternal()](passive/getPressureInternal.md)
- [getTemperature()](passive/getTemperature.md)
- [getAllSensorData()](passive/getAllSensorData.md)
- [setLoggingLevel( level )](configuration/setLoggingLevel.md)
- [setRecordingInterval( sensor, interval )](configuration/setRecordingInterval.md)
- [setDefaultQueueMode( mode )](configuration/setDefaultQueueMode.md)
- getSonarMap()
- All GPS-Related functions, including:
  - setGpsMode()
  - getCoordinates()
  - goToCoordinates()
  - setHome()
  - goToHome()
