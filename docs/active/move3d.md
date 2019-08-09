# move3d( throttleX, throttleY, throttleZ, time, execMode \<optional> )

This function moves the drone in 3 dimensions in a given direction for a specified period of time.

## Parameters

throttleX (integer):  
> An integer from -100 to 100 indicating the percent throttle to use in the X direction

throttleY (integer):  
> An integer from -100 to 100 indicating the percent throttle to use in the Y direction

throttleZ (integer):  
> An integer from -100 to 100 indicating the percent throttle to use in the Z direction

time (float):  
> An real number representing the time in seconds between activation and deactivation of the propellers

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
MLI.move3d(throttleX=100, throttleY=100, throttleZ=0, time = 15)
# Moves the drone forward and to the right at 100% power for 15 seconds

MLI.move3d(0, 0, 100, 10)
# Thrust upward for 10 seconds
```

## Related Mavlink Messages

- MANUAL_CONTROL
