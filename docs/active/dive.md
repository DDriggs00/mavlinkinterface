# dive( depth, throttle \<optional> )

This call is used to change the depth of the drone.

## Parameters

depth (float):  
> The distance to dive in meters.  
> Negative numbers indicate an increase in depth.

throttle (int, optional):
> The percentage of vertical thrust to use.  
> Default is 100

## Return Values

Returns void

## Examples

```py
dive(depth = -10)
# The drone descends by 10 meters or until it is obstructed

dive(depth = 10, throttle = 50)
# The drone ascends by 10 meters at 50 percent throttle or until it is obstructed

dive(depth = 5, absolute)
# An exception is thrown, indicating that the drone cannot rise above the surface of the water
```
