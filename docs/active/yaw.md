# yaw( degrees, absolute \<optional>, execMode \<optional> )

Relative: yaws the drone in place by *degrees*  degrees  
Absolute: yaws the drone to face in the direction *degrees* degrees

Note: This command will not rotate the drone by more than 180 degrees in either direction.  
See examples below for how this is implemented.

## Parameters

degrees (integer)
> An integer for how many degrees to rotate
> If a number greater than 360 if given, it will be reduced to the lowest equivalent angle.

absolute (boolean, optional):
> When true, *degrees* is relative to magnetic north  
> When false or absent, *degrees* is relative to the current heading of the drone

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

Returns void.

## Examples

```py
MLI.yaw(degrees = 15)
# Result: The drone yaws to the right by 15 degrees

MLI.yaw(degrees = 270)
# Result: The drone yaws to the left by 90 degrees

MLI.yaw(degrees = -410)
# Result: The drone yaws to the left by 50 degrees

MLI.yaw(degrees = -15, absolute)
# Result: The drone yaws the shortest distance to face 15 degrees to the left of magnetic north
```

## Related Mavlink Messages

- MANUAL_CONTROL
