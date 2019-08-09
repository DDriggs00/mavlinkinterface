# move( direction, time, throttle \<optional>, absolute \<optional>, execMode \<optional> )

This function moves the drone across the X/Y plane in a specified direction for a specified time.

## Parameters

direction (integer):  
> An integer indicating the direction in degrees the drone will be moving.

time (float):  
> An real number representing the time in seconds between activation and deactivation of the propellers

throttle (integer, optional):  
> An integer from 1 to 100 representing the percentage of propeller power to use.  
> Defaults to 50

absolute (boolean, optional):
> When true, *direction* is relative to magnetic north  
> When false or absent, *direction* is relative to the current heading of the drone

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

## Examples

```py
MLI.move(direction = 0, time = 15, throttle = 75)
# Moves the drone straight forward at 75% power for 15 seconds

MLI.move(direction = -15, time = 0.5, absolute=True)
# moves in the direction of 15 degrees to the right of magnetic north at 100% power for half a second
```

## Related Mavlink Messages

- MANUAL_CONTROL
