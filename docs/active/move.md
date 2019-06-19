# move( direction, time, throttle \<optional> )

Move the drone *direction* at *throttle* percent power for *time* seconds

## Parameters

direction (integer):  
> An integer indicating the direction in degrees the drone will be moving.

time (float):  
> An real number representing the time in seconds between activation and deactivation of the propellers

throttle (integer, optional):  
> An integer from 1 to 100 representing the percentage of propeller power to use.  
> Defaults to 100

## Return Values

Returns a string.  
If the action completed successfully, returns "Success"  
If the action failed, returns the reason and time (in seconds from start) of failure

## Examples

```py
move(direction = 0, time = 15, throttle = 75)
# Moves the drone straight forward at 75% power for 15 seconds

move(direction = -15, time = 0.5, absolute)
# moves in the direction of 15 degrees to the right of magnetic north at 100% power for half a second
```
