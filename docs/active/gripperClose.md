# gripperClose( time, execMode \<optional> )

Close the grabber arm by *percent*% or until gripping an object with *strength*% strength

## Parameters

time (float):  
> The number of seconds to send the "close" signal to the gripper arm

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
MLI.gripperClose(0.5)
# The grabber arm closes for 1/2 second
```