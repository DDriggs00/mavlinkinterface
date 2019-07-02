# Current Status

## Completed functions

These functions perform exactly as described in the readme

- [arm()](active/arm.md)
- [disarm()](active/disarm.md)
- [setFlightMode( flightMode, execMode \<optional> )](active/setFlightMode.md)
- [move( direction, time, throttle \<optional>, absolute \<optional>, execMode \<optional> )](active/move.md)
- [move3d( throttleX, throttleY, throttleZ, time, execMode \<optional> )](active/move3d.md)
- [surface( execMode \<optional> )](active/surface.md)
- [setLights( brightness, execMode \<optional> )](active/lights.md)
- [getDepth()](passive/getDepth.md)
- [getGyroscopeData()](passive/getGyroscopeData.md)
- [getAccelerometerData()](passive/getAccelerometerData.md)
- [getBatteryData()](passive/getBatteryData.md)
- [getHeading()](passive/getHeading.md)
- [getMagnetometerData()](passive/getMagnetometerData.md)
- [getPressureExternal()](passive/getPressureExternal.md)

## New Functions

These functions were not originally intended, but were added

- [setSurfacePressure( pressure \<optional> )](configuration/setSurfacePressure.md)
  - This was needed for the getDepth() function
- [setFluidDensity( density \<optional> )](configuration/setFluidDensity.md)
  - This was needed for the getDepth() function (salt vs fresh water)

## Partially completed functions

These functions work as described in the documentation, but to a lesser grade of accuracy. Details on the failings of each one included. These are actively under development

- [dive( depth, throttle \<optional>, absolute \<optional>, execMode \<optional> )](active/dive.md)
- [yaw( degrees, absolute \<optional>, execMode \<optional> )](active/yaw.md)

## Modified Functions (complete)

These Functions were changed in a major way, which is explained below.

- [gripperOpen( time, execMode \<optional> )](active/gripperOpen.md)
  - The gripper arm can only be controlled by a pwm channel with 2 settings: Open, and close.  Due to this, the function is less featured than anticipated.
- [gripperClose( time, execMode \<optional> )](active/gripperClose.md)
  - The gripper arm can only be controlled by a pwm channel with 2 settings: Open, and close.  Due to this, the function is less featured than anticipated.
- [setLeakAction( action )](configuration/setLeakAction.md)
  - The leak sensor works oddly, in that it is silent until it detects a leak, at which point it is sends a STATUSTEXT message of "Leak Detected!". Due to this, this function is a thread that continuously checks the statusText and reads those messages.  setLeakAction is used to set the behavior upon encountering a leak.

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
