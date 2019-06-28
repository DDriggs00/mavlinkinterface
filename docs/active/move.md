# move( direction, time, throttle \<optional>, execMode \<optional> )

Move the drone *direction* at *throttle* percent power for *time* seconds

## Parameters

direction (integer):  
> An integer indicating the direction in degrees the drone will be moving.

time (float):  
> An real number representing the time in seconds between activation and deactivation of the propellers

throttle (integer, optional):  
> An integer from 1 to 100 representing the percentage of propeller power to use.  
> Defaults to 100

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
move(direction = 0, time = 15, throttle = 75)
# Moves the drone straight forward at 75% power for 15 seconds

move(direction = -15, time = 0.5, absolute)
# moves in the direction of 15 degrees to the right of magnetic north at 100% power for half a second
```
