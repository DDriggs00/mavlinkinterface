# surface( execMode \<optional> )

This function brings the drone to the surface at full throttle.

## Parameters

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
MLI.surface()
# The drone ascends to the surface
```

## Related Mavlink Messages

- MANUAL_CONTROL
