# disarm(execMode \<optional>)

Disables the propellers

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

Returns void

## Examples

```py
MLI.disarm()
# The propellers are now disabled.
# Due to the way the ArduSub works, movement commands will still be sent, but will not do anything.
```

## Related Mavlink Commands

- MAV_CMD_COMPONENT_ARM_DISARM
