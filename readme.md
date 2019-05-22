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

## Architecture
* Written using Python 3.7 latest
* Dependencies
    * [pymavlink](https://github.com/ArduPilot/pymavlink)

# Active Calls

## rotate( degrees )
Relative: Rotates the submarine in place by *degrees*  degrees  
Absolute: Rotates the submarine to face in the direction *degrees* degrees

### Arguments:
degrees (integer)
: An integer for how many degrees to rotate
: In absolute mode, this is limited to between 0 and 360.

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
Move the submarine *direction* at *throttle* percent power for *time* seconds

### Arguments:
direction (integer):  
: An integer indicating the direction in degrees the submarine will be moving.

time (float):  
: An real number representing the time in seconds between activation and deactivation of the propellers

throttle (integer, optional):  
: An integer from 1 to 100 representing the percentage of propeller power to use.
: Defaults to 100

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
: The distance to dive in feet.
: In relative mode, negative numbers can be used to rise.

### Return Values  
Returns a string.  
If the action succeeded, returns "Success,  *new\_depth*"  
If the action failed, returns teh reason for failure and the new depth

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
Close the grabber arm by *percent*% or until gripping an object with *strength*% strength

### Arguments
strength (integer, optional):  
: An integer from 1 to 100 representing the percentage of motor strength to use in gripping.
: Defaults to 100%

percent (integer, optional):  
: An integer from 1 to 100 representing the amount, as a percentage of the whole distance, the arm should close

### Return Values
Returns a string.  
Upon success, returns "Success"  
Upon failure, returns the reason for failure  
Note: If arm is overheating, or would overheat following the next action, no action will be taken and function will return "Overheating, No Action Taken".

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
Open the grabber arm by *percent*%

### Arguments
percent (integer, optional):  
: An integer from 1 to 100 representing the amount, as a percentage of the whole distance, the arm should close

### Return Values
Returns a string.  
Upon success, returns "Success"  
Upon failure, returns the reason for failure  
Note: If arm is overheating, or would overheat following the next action, no action will be taken and function will return "Overheating, No Action Taken".

### Examples
```py
armRelease
# The grabber arm opens completely

armRelease(10)
# The grabber arm opens by 10%
```
## lights( brightness )
Sets the lights to a specific brightness

### Arguments
brightness (integer):  
: An integer from 0 to 100, representing the percent brightness of the lights.

### Return Values:
Returns a string.  
Upon success, returns "Success"  
Upon Failure, returns the reason for failure.

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
: An integer from -180 to 180 (-90 to 90 in Absolute mode) representing the number of degrees to tilt the camera, with up being positive.
: In absolute mode, 0 is directly forward.

speed (integer, optional):  
: An integer from 1 to 100 representing the percentage of total velocity to use when rotating the camera. Useful for panning when taking video.
: Default is 100.

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
Enables the propellors if the pre-arm safety checks pass. 

### Return Values
Returns a string.  
Upon success or failure, returns the success/fail status, and each of the pre-arm safety checks, their pass/fail status, and their return values

### Example
arm command is run and fails, output:
```json
{
    "state":"Success",
    "checks": {
        "check1": {
            "state":"Pass",
            "output": 1234
        },
        "check2": {
            "state":"Fail",
            "output": 1234
        },
        "check3": {
            "state":"Pass",
            "output": "check 3 return value"
        }
    }
}
```
## disarm()
Disables the propellors

### Return Values
Returns a string.  
Upon success, returns "Success"  
Upon Failure, Returns the reason for failure

### Examples
```py
disarm
# The propellors disable, returns "Success"
```
## Universal Arguments

### BlockMode (enum)  
This argument prevents all other active calls until the paired command has been finished or aborted.  
* When None, any other action commands will override and stop the command.  
* When Queue, other action commands will be queued behind the command.  
* When Block, other action commands will be ignored until the command completes  
* When this argument is not present, it will be treated as None (configurable)

### Override (switch)
When present, this argument causes any currently executing or queued commands to stop, and this command will to executed immediately.  This can also be used to force an arming of the propellors.

### Absolute (switch)
This argument causes movement commands to use absolute coordinates and directions, rather than coordinates and directions relative to the submarine.
* When present, direction is relative to magnetic north, depth is relative to the surface, etc.
* When absent, direction coordinates, depth, and distances are all relative to the submarine's current location and the direction it is facing
Note: This argument is only relevant where a direction, depth, or coordinates are present

# Passive Calls
## cameraStartFeed()
Creates a camera feed that the controller can access.

### Return Values
Returns a string.  
Upon Success, returns all information neccesary to access the video stream.  
Upon failure, returns the reason for failure.

### Examples
```py
cameraStartFeed
# The camera feed is enabled and the following JSON returned
```
```json
{
    "state":"Success",
    "ip":"Stream IP",
    "port":"Stream Port"
    ...
}
```
## cameraVideoStart( time \<optional>, resolution \<optional> )
Starts the camera recording video. The video will end when either the cameraVideoStop is called, the optional timer ends, or the internal storage runs out.

### Arguments
time (integer, optional):  
: The number of seconds to record video before automatically ending

resolution (string, optional):  
: Used to reduce the resolution the camera is recording at. Default is 1080p (camera max)

### Return Values
Returns a JSON-formatted string string.  
Upon success, returns the local path of the video.  
Upon failure, returns the reason for failure.

### Examples
```py
cameraVideoStart
# Starts the video feed to record until stopped at 1080p, returns the following JSON
```
```json
{
    "state":"Success",
    "path":"/.../video/2019-05-22T08.48.34.mp4"
}
```
```py
cameraVideoStart(time = 3600, resolution = '720p') 
# Starts the video feed to record for up to 1 hour at 720p, but fails due to a lack of storage space and returns the following JSON
```
```json
{
    "state":"Failure",
    "failReason":"Lack of storage space"
}
```
## cameraVideoStop()
Ends the current video if recording is active

### Return Values
Returns a string.  
Upon Success, Returns "Success"  
Upon Failure, returns failure reason

### Examples
```py
cameraVideoStop # Assuming video is recording
# The currently recording video ends and the video file is finalized, and returns "Success"
cameraVideoStop # Assuming video is not recording
# The currently recording video ends and the video file is finalized, and function returns "Failed, No video to stop"
```
## cameraPhoto( resolution \<optional>, zoom \<optional>, )
Takes a photo using the camera and returns its path.

### Arguments
resolution (string, optional):  
: Used to reduce the resolution the camera is recording at. Default is 1080p (camera max)

### Return Values
Returns a JSON-formatted string string.  
Upon success, returns the local path of the image.  
Upon failure, returns the reason for failure.

### Examples
```py
cameraPhoto
# Captures a 1080p photo, and returns the following JSON
```
```json
{
    "state":"Success",
    "path":"/.../images/2019-05-22T08.48.34.jpg"
}
```
```py
cameraPhoto(resolution = '720p') 
# takes a 720p photo, but fails due to a lack of storage space and returns the following JSON
```
```json
{
    "state":"Failure",
    "failReason":"Lack of storage space"
}
```
## getLeakData()
## getDepth()
## getPressure()
## getInternalPressure()
## GetTemperature()
## getBearing()
## getAccelerometerData()
## getGyroscopeData()
## GetBatteryData()
## getSonarMap
## getAllSensorData
## getAllPassiveSensorData

# Configuration Calls

## enableLogging( sensor )
## disableLogging( sensor )
## setDefaultBlockMode()