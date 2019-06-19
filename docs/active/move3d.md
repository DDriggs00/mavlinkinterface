# move( throttleX, throttleY, throttleZ, time )

Move the drone in a given direction and power level for *time* seconds

## Parameters

throttleX (integer):  
> An integer from -100 to 100 indicating the percent throttle to use in the X direction

throttleY (integer):  
> An integer from -100 to 100 indicating the percent throttle to use in the Y direction

throttleZ (integer):  
> An integer from -100 to 100 indicating the percent throttle to use in the Z direction

time (float):  
> An real number representing the time in seconds between activation and deactivation of the propellers

## Return Values

Returns void

## Examples

```py
move3d(throttleX=100, throttleY=100, throttleZ=0, time = 15)
# Moves the drone forward and to the right at 100% power for 15 seconds
```
