# cameraTilt( angle, speed <optional> )
Tilts the camera by the angle specified. Range is +/- 90 degrees.

## Parameters
angle (integer):  
> An integer from -180 to 180 (-90 to 90 in Absolute mode) representing the number of degrees to tilt the camera, with up being positive.  
> In absolute mode, 0 is directly forward.

speed (integer, optional):  
> An integer from 1 to 100 representing the percentage of total velocity to use when rotating the camera. Useful for panning when taking video.  
> Default is 100.

## Return Values
Returns a string.  
Upon completing the desired rotations, returns "Success"  
If the action could not be completed, returns the reason for failure and the new angle

## Examples
```py
cameraTilt(angle = -45) # Assuming camera is flat
# Rotates the camera downward by 45 degrees at full speed and returns True

cameraTilt(angle = 110, speed = 10) # Assuming camera is flat
# Rotates the camera upward at 10% of maximum speed until it reaches the limit of +90 degrees, Returns "Reached max angle. Angle=90"

cameraTilt(angle = 0, absolute)
# Positions the camera to point straight forward, Returns True
```

MAV_CMD_DO_MOUNT_CONFIGURE  
MAV_CMD_DO_MOUNT_CONTROL  
MAV_CMD_DO_MOUNT_CONTROL_QUAT 