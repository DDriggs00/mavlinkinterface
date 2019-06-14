# dive( time, throttle \<optional> )

This call is used to change the depth of the submarine.

## Parameters

time (float):  
> The time to dive in seconds

throttle (int)
> The percentage throttle to use when diving.  
> Negative numbers indicate an increase in depth.

## Return Values

Returns void.  

## Examples

```py
dive(depth = -10)
# The submarine descends by 10 meters or until it is obstructed

dive(depth = 10)
# The submarine ascends by 10 meters or until it surfaces or is obstructed

dive(depth = 5, absolute)
# The submarine moves to a depth of 5 meters below the surface or until it is obstructed
```

# dive( depth ) \<future>

This call is used to change the depth of the submarine.

## Parameters

depth (float):  
> The distance to dive in meters.  
> Negative numbers indicate an increase in depth.

## Return Values

Returns a string.  
If the action succeeded, returns "Success,  *new\_depth*"  
If the action failed, returns the reason for failure and the new depth

## Examples

```py
dive(depth = -10)
# The submarine descends by 10 meters or until it is obstructed

dive(depth = 10)
# The submarine ascends by 10 meters or until it surfaces or is obstructed

dive(depth = 5, absolute)
# The submarine moves to a depth of 5 meters below the surface or until it is obstructed
```
