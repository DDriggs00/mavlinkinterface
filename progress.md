# Current Status

## Completed functions

These functions perform exactly as described in the readme

- [arm()](docs/active/arm.md)
- [disarm()](docs/active/disarm.md)
- [setFlightMode( mode )](docs/active/setFlightMode.md)
- [move( direction, time, throttle \<optional> )](docs/active/move.md)
- [move3d( throttleX, throttleY, throttleZ, time )](docs/active/move3d.md)
- [surface()](docs/active/surface.md)
- [setLights( brightness )](docs/active/setLights.md)
- [getDepth()](docs/passive/getDepth.md)
- [getGyroscopeData()](docs/passive/getGyroscopeData.md)
- [getAccelerometerData()](docs/passive/getAccelerometerData.md)
- [getBatteryData()](docs/passive/getBatteryData.md)
- [getHeading()](docs/passive/getHeading.md)
- [getMagnetometerData()](docs/passive/getMagnetometerData.md)
- [getPressureExternal()](docs/passive/getPressureExternal.md)

## New Functions

These functions were not originally intended, but were added

- setSurfacePressure()
  - This was needed for the getDepth() function
- setFluidDensity()
  - This was needed for the getDepth() function (salt vs fresh water)

## Partially completed functions

These functions work as described in the documentation, but to a lesser grade of accuracy. Details on the failings of each one included. These are actively under development

- [dive( depth, throttle \<optional> )](docs/active/dive.md)
- [yaw( degrees )](docs/active/yaw.md)

## Modified Functions

These Functions were changed in a major way due to the method of communication

- [gripperOpen( time )](docs/active/armRelease.md)
  - The gripper arm can only be controlled by a pwm channel with 2 settings: Open, and close.  Due to this, the function is less featured than anticipated.
- [gripperClose( time )](docs/active/armGrab.md)
  - The gripper arm can only be controlled by a pwm channel with 2 settings: Open, and close.  Due to this, the function is less featured than anticipated.
- [getLeakData()](docs/passive/getLeakData.md)
  - The leak sensor works oddly, in that it is silent until it detects a leak, at which point it is sends a STATUSTEXT message of "Leak Detected!". Due to this, this function is a thread that continuously checks the statusText and reads those messages.

## Not Started functions

- [cameraTilt( angle, speed \<optional> )](docs/active/cameraTilt.md)
- [cameraStartFeed()](docs/passive/cameraStartFeed.md)
- [cameraVideoStart( time \<optional>, resolution \<optional> )](docs/passive/cameraVideoStart.md)
- [cameraVideoStop()](docs/passive/cameraVideoStop.md)
- [cameraPhoto( resolution \<optional>, zoom \<optional>, )](docs/passive/cameraPhoto.md)
- [getPressureInternal()](docs/passive/getPressureInternal.md)
- [getTemperature()](docs/passive/getTemperature.md)
- [getAllSensorData()](docs/passive/getAllSensorData.md)
- getSonarMap()
- All GPS-Related functions, including:
  - setGpsMode()
  - getCoordinates()
  - goToCoordinates()
  - setHome()
  - goToHome()
- [setLoggingInterval( level )](docs/configuration/setLoggingLevel.md)
- [setRecordingInterval( sensor, interval )](docs/configuration/setRecordingInterval.md)
- [setDefaultQueueMode( mode )](docs/configuration/setDefaultQueueMode.md)
