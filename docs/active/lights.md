# setLights( brightness )

Sets the lights to a specific brightness

## Parameters

brightness (integer):  
> An integer from 0 to 100, representing the percent brightness of the lights.

## Return Values

Returns a string.  
Upon success, returns "Success"  
Upon Failure, returns the reason for failure.

## Examples

```py
setLights(0)
# Turns the lights off

setLights(65)
# sets the lights to 65% brightness

setLights(100)
# sets the lights to full brightness
```
