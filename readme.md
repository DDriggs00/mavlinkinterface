# Catfish API


## Features

* Python!
* Full Logging of some or all sensor data (configurable)
* All functions return either:
    1. a single variable
    1. A JSON string
* All physical commands have blocking, queueing, and regular modes, as well as  an override system
* Movement Commands can detect blockage
* All sensor info accessible individually or aggregately


# Active Calls
## rotate( degrees )
Relative: Rotates the submarine in place by _degrees_  degrees  
Absolute: Rotates the submarine to face in the direction _degrees_ degrees

### Arguments:
degrees (integer):  
An integer for how many degrees to rotate. In absolute mode, this is limited to between 0 and 360.

### Return Values
Returns a string.  
Upon completing the desired rotations, returns "Success"  
If the action could not be completed (eg. Obstruction, overridden), returns the reason for failure and the new bearing

### Examples:
```py
rotate(degrees = 15)
# Result: The submarine rotates to the right by 15 degrees

rotate(degrees = -720)
# Result: The submarine rotates to the left by 2 full rotations

rotate(degrees = -15, absolute)
# Result: The submarine rotates the shortest distance to face 15 degrees to the left of magnetic north
```
## move( direction, time, throttle \<optional> )
Move the submarine _direction_ at _throttle_ percent power for _time_ seconds

### Arguments:
direction (integer):  
An integer indicating the direction in degrees the submarine will be moving.

time (float):  
An real number representing the time in seconds between activation and deactivation of the propellers

throttle (integer, optional):  
An integer from 1 to 100 representing the percentage of propeller power to use. Defaults to 100

### Return Values:
Returns a string.  
If the action completed successfully, returns "Success"  
If the action failed, returns the reason and time (in seconds from start) of failure

### Examples:
```py
move(direction = 0, time = 15, throttle = 75)
# Moves the submarine straight forward at 75% power for 15 seconds

move(direction = -15, time = 0.5, absolute)
# moves in the direction of 15 degrees to the right of magnetic north at 100% power for half a second
```
## dive( depth )
This call is used to change the depth of the submarine. It returns true upon success, and false upon obstruction or surfacing

### Arguments:
depth (float):  
The distance to dive in feet. In relative mode, negative numbers can be used to rise.

### Return Values  
Returns a string.  
If the action succeeded, returns "Success,  _new\_Height_

### Examples:
```py
dive(depth = 10)
# The submarine descends by 10 feet or until it is obstructed

dive(depth = -10)
# The submarine ascends by 10 feet or until it surfaces or is obstructed

dive(depth = 5, absolute)
# The submarine moves to a depth of 5 feet below the surface or until it is obstructed
```
## surface()
This call brings the submarine to the surface. It returns True upon success and False upon obstruction.

### Return Values:
Returns a string.  
Upon success, returns "Success"  
Upon Failure, returns the reason for failure and the new depth

### Example
```py
surface
# The submarine ascends to the surface
```
## armGrab( strength \<optional>, percent \<optional> )
Close the grabber arm by _percent_% or until gripping an object with _strength_% strength

### Arguments
strength (integer, optional):  
An integer from 1 to 100 representing the percentage of motor strength to use in gripping. Defaults to 100%

percent (integer, optional):  
An integer from 1 to 100 representing the amount, as a percentage of the whole distance, the arm should close

### Return Values
Returns a string.  
Upon success, returns "Success"  
Upon failure, returns the reason for failure  
Note: If arm is overheating, no action will be taken and function will return "Overheating".

### Examples
```py
armGrab()
# The grabber arm closes until either closed or gripping an object with 100% strength

armGrab(strength = 50)
# The grabber arm closes until either closed or gripping an object with 50% strength

armGrab(strength = 100, percent = 50)
# The grabber arm closes by 50% or until closed or gripping an object with full strength
```
## armRelease( percent \<optional> )
Open the grabber arm by _percent_%

### Arguments
percent (integer, optional):  
An integer from 1 to 100 representing the amount, as a percentage of the whole distance, the arm should close

### Return Values
Returns a string.  
Upon success, returns "Success"  
Upon failure, returns the reason for failure  
Note: If arm is overheating, no action will be taken and function will return "Overheating".

### Examples
```py
armRelease
# The grabber arm opens comletely

armRelease(10)
# The grabber arm opens by 10%
```
## lights( brightness )
Sets the lights to a specific brightness

### Arguments
brightness (integer):  
An integer from 0 to 100, representing the percent brightness of the lights.

### Return Values:
Returns a string.  
Upon success, returns "Success"  
Upon Failure, returns theaa reason for failure.

### Examples
```py
lights(0)
# Turns the lights off

lights(65)
# sets the lights to 65% brightness

lights(100)
# sets the lights to full brightness
```
## cameraTilt( angle, speed <optional> )
Tilts the camera by the angle specified. Range is +/- 90 degrees.

### Arguments
angle (integer):  
An integer from -180 to 180 (-90 to 90 in Absolute mode) representing the number of degrees to tilt the camera, with up being positive.  In absolute mode, 0 is directly forward.

speed (integer, optional):  
An integer from 1 to 100 representing the percentage of total velocity to use when rotating the camera. Useful for panning when taking video. Default is 100.

### Return Values
Returns a string.  
Upon completing the desired rotations, returns "Success"  
If the action could not be completed, returns the reason for failure and the new angle

### Examples
```py
cameraTilt(angle = -45) # Assuming camera is flat
# Rotates the camera downward by 45 degrees at full speed and returns True

cameraTilt(angle = 110, speed = 10) # Assuming camera is flat
# Rotates the camera upward at 10% of maximum speed until it reaches the limit of +90 degrees, Returns "Reached max angle. Angle=90"

cameraTilt(angle = 0, absolute)
# Positions the camera to point straight forward, Returns True
```
## arm()
## disarm()
## Universal Arguments

### BlockMode (enum)  
This argument prevents all other active calls until the paired command has been finished or aborted.  
* When None, any other action commands will override and stop the command.  
* When Queue, other action commands will be queued behind the command.  
* When Block, other action commands will be ignored until the command completes  
* When this argument is not present, it will be treated as None (configurable)

### Override (switch)
When present, this argument causes any currently executing or queued commands to stop, and this command will to executed immidiately. Primarily designed for emergency surfacing.

### Absolute (switch)
This argument causes movement commands to use absolute coordinates and directions, rather than coordinates and directions relative to the submarine.
* When present, direction is relative to magnetic north, depth is relative to the surface, etc.
* When absent, direction coordinates, depth, and distances are all relative to the submarine's current location and the direction it is facing
Note: This argument is only relevant where a direction, depth, or coordinates are present

# Passive Calls

## cameraVideoStart( resolution \<optional> )
Starts the camera recording video. The video will end when either the cameraVideoStop is called or

### Arguments
arg (type):  
description

### Examples
```py

```
## cameraVideoStop()

## takePhoto
Takes a photo using the camera and returns its path.

### Arguments
// Advanced args go here

### Examples
```py

```
## getSonarMap
## getAllSensorData
## getAllPassiveSensorData
## getDepth()
## getPressure()
## getInternalPressure()
## GetTemperature()
## getAccelerometerData()
## getGyroscopeData()
## getBearing()
## getLeakData()
## GetBatteryData()

# Configuration Calls

## enableLogging( sensor )
## disableLogging( sensor )
## setDefaultBlockMode()