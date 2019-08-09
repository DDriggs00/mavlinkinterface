# gripperOpen( time, execMode \<optional> )

Power the gripper arm open for *time* seconds  
Opening the gripper from a fully closed position is 1.75 sec

## Parameters

time (float):  
> The number of seconds to send the "close" signal to the gripper arm  
> This has a resolution of 0.25 sec.  
> Fully opening the gripper is 1.75 sec

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
MLI.gripperOpen(0.5)
# The grabber arm powers open for 1/2 second

MLI.gripperOpen(1.75)
# The grabber arm powers open for 1 3/4 seconds
```

## Related Mavlink Messages

- MANUAL_CONTROL
