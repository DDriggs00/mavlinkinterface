# DEPRECATED: wait( time, execMode \<optional> )

This function is functionally identical to sleep(), except it is able to be used with queue modes

## Parameters

time (float):
> The amount of time to wait.

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
# This is an example for which a wait is useful.
for i in range(3)
    MLI.dive(depth=-1, execMode='queue')
    MLI.wait(3, execMode='queue')
```
