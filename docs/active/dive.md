# dive( depth, throttle \<optional>, absolute \<optional>, execMode \<optional> )

This call is used to change the depth of the drone.

## Parameters

depth (float):  
> The distance to dive in meters.  
> Negative numbers indicate an increase in depth.

throttle (int, optional):
> The percentage of vertical thrust to use.  
> Default is 50

absolute (boolean, optional):
> When true, *depth* signifies the target depth, rather than the change in depth

execMode (string, optional):
> The execution mode to use for this command. Possible execution modes are:
>
> 1. Synchronous
> 1. Queue
> 1. Ignore
> 1. Override
>
> If not given, defaults to the execution mode given on class initiation.  
> For details on how these modes work, see [Here](../executionModes.md)

## Return Values

Returns void  
If the given values would put the drone above the surface, throws a ValueError

## Examples

```py
MLI.dive(depth = -10)
# The drone descends by 10 meters or until it is obstructed

MLI.dive(depth = 9, throttle = 100)
# The drone ascends by 9 meters at 100 percent throttle or until it is obstructed

MLI.dive(depth = -5, absolute=True)
# The drone ascends or descends until it reaches a depth of 5 meters below the surface

MLI.dive(depth = 5, absolute=True)
# An ValueError is thrown, indicating that the drone cannot rise above the surface of the water
```

## Related Mavlink Messages

- MANUAL_CONTROL
