# yaw( degrees )

Relative: yaws the drone in place by *degrees*  degrees  
Absolute: yaws the drone to face in the direction *degrees* degrees

## Parameters

degrees (integer)
> An integer for how many degrees to rotate
> In absolute mode, this is limited to between 0 and 360.

## Return Values

Returns a string.  
Upon completing the desired rotations, returns "Success"  
If the action could not be completed (eg. Obstruction, overridden), returns the reason for failure and the new heading

## Examples

```py
rotate(degrees = 15)
# Result: The drone yaws to the right by 15 degrees

rotate(degrees = -720)
# Result: The drone yaws to the left by 2 full rotations

rotate(degrees = -15, absolute)
# Result: The drone yaws the shortest distance to face 15 degrees to the left of magnetic north
```
