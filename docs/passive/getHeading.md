# getHeading()

This function uses the IMU magnetometer to calculate the direction the drone is facing.

## Return Values

Returns a float.  
Returns the heading of the drone in degrees (as the smallest possible positive value).

## Examples

```py
MLI.getHeading() # assuming the drone is facing due north
# returns 0

MLI.getHeading() # assuming the drone is facing due east
# returns 90
```
