# wait( time, execMode \<optional> )

This call gives an empty manual control message to the drone to prevent the interruption of the manual control heartbeat.  
This is required if a rest is needed while no manual control is being sent.

## Parameters

time (float):
> The amount of time to wait.  
> The time parameter has a resolution of .25 seconds.

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

## Example

```py
# This is an example which requires a wait (a sleep function will not work properly).
for i in range(3)
    MLI.dive(depth=-1, execMode='queue')
    MLI.wait(3, execMode='synchronous')
    # Collect data
```

```py
# This is an example which requires a wait (a sleep function will not work properly).
for i in range(3)
    MLI.dive(depth=-1, execMode='queue')
    MLI.wait(3, execMode='queue')

# collect data
```

```py
# This is an example which does not require the wait function
mli.move(direction=0, time=10, execMode='queue')
sleep(7)    # because the movement function is still executing in the background, this is a sleep
# Do something
```

## Related Mavlink Messages

- MANUAL_CONTROL
