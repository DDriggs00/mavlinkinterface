# setLights( brightness, execMode \<optional> )

This function sets brightness of the lights.

## Parameters

brightness (integer):  
> An integer from 0 to 100, representing the percent brightness of the lights.  
> This will be rounded to the nearest allowed lighting level.

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
MLI.setLights(0)
# Turns the lights off

MLI.setLights(65)
# sets the lights to 65% brightness

MLI.setLights(brightness=100)
# sets the lights to full brightness
```

## Related Mavlink Messages

- MANUAL_CONTROL
