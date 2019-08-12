# getDepth()

This function calculates the depth based on the external pressure sensor data.

## Return values

Returns a float
Returns the depth of the drone as distance from the surface in meters

## Examples

```py
MLI.getDepth() # Assuming the drone is surfaced
# returns 0

MLI.getDepth() # Assuming the drone is 5.4 meters below the surface
# returns 5.4
```
