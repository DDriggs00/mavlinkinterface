# arm( execMode \<optional> )

This function enables the thrusters, allowing movement commands to work.

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
MLI.arm()
# The propellors are now armed
```

## Related Mavlink Commands

- MAV_CMD_COMPONENT_ARM_DISARM
