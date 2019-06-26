# Current Status

## Completed functions

These functions perform exactly as described in the readme

- [arm()](docs/Active/arm.md)
- [disarm()](docs/Active/disarm.md)
- [setFlightMode( mode )](docs/Active/setFlightMode.md)
- [move( direction, time, throttle \<optional> )](docs/Active/move.md)
- [move3d( throttleX, throttleY, throttleZ, time )](docs/Active/move3d.md)
- [surface()](docs/Active/surface.md)
- [setLights( brightness )](docs/Active/setLights.md)
- [getDepth()](docs/Passive/getDepth.md)
- [getGyroscopeData()](docs/Passive/getGyroscopeData.md)
- [getAccelerometerData()](docs/Passive/getAccelerometerData.md)
- [getBatteryData()](docs/Passive/getBatteryData.md)
- [getHeading()](docs/Passive/getHeading.md)
- [getMagnetometerData()](docs/Passive/getMagnetometerData.md)
- [getPressureExternal()](docs/Passive/getPressureExternal.md)

## New Functions

These functions were not originally intended, but were added

## Partially completed functions

These functions work as described in the documentation, but to a lesser grade of accuracy. Details on the failings of each one included. These are actively under development

- [dive( depth, throttle \<optional> )](docs/Active/dive.md)
- [yaw( degrees )](docs/Active/yaw.md)

## Modified Functions

These Functions were changed in a major way due to the method of communication

- [gripperOpen( time )](docs/Active/armRelease.md)
  - The gripper arm can only be controlled by a pwm channel with 2 settings: Open, and close.  Due to this, the function is less featured than anticipated.
- [gripperClose( time )](docs/Active/armGrab.md)
  - The gripper arm can only be controlled by a pwm channel with 2 settings: Open, and close.  Due to this, the function is less featured than anticipated.
- [getLeakData()](docs/Passive/getLeakData.md)
  - The leak sensor works oddly, in that it is silent until it detects a leak, at which point it is sends a STATUSTEXT message of "Leak Detected!". Due to this, this function is a thread that continuously checks the statusText and reads those messages.

## Not Started functions

- [cameraTilt( angle, speed \<optional> )](docs/Active/cameraTilt.md)
- [cameraStartFeed()](docs/Passive/cameraStartFeed.md)
- [cameraVideoStart( time \<optional>, resolution \<optional> )](docs/Passive/cameraVideoStart.md)
- [cameraVideoStop()](docs/Passive/cameraVideoStop.md)
- [cameraPhoto( resolution \<optional>, zoom \<optional>, )](docs/Passive/cameraPhoto.md)
- [getPressureInternal()](docs/Passive/getPressureInternal.md)
- [getTemperature()](docs/Passive/getTemperature.md)
- [getAllSensorData()](docs/Passive/getAllSensorData.md)
- getSonarMap()
- All GPS-Related functions, including:
  - setGpsMode()
  - getCoordinates()
  - goToCoordinates()
- [setLoggingInterval( level )](docs/Configuration/setLoggingLevel.md)
- [setRecordingInterval( sensor, interval )](docs/Configuration/setRecordingInterval.md)
- [setDefaultQueueMode( mode )](docs/Configuration/setDefaultQueueMode.md)


TODO: add pitch, roll, setThrust, setAltitudeTarget

X: Item is not yet Implemented  
B: A Basic version has been Implemented
