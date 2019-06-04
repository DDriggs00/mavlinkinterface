# setLoggingLevel( sensor, level )

Modifies the level of logging done on a sensor.

## Parameters

sensor (string):
> The sensor or other data input source for which to modify the entry.

level (enum):
> The level of logging to perform. Possible levels are:  
> Full: Records all data from every sensor input instance  
> Off: No logs of sensor data are kept except by explicit instruction

## Return Values

Returns void

## Examples

```py
setLoggingLevel( sensor = TEMP_01, level = Full)
 # Sets the temperature sensor with ID TEMP_01 to perform full logging
```
