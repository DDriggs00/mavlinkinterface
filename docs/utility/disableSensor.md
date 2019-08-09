# disableSensor( sensor, enable \<optional> )

This function is used to disable certain sensors to simulate a sensor failure.

## Parameters

sensor (str):
> The sensor to disable
> Valid options are: pressure, gps, sonar

enable (bool, optional):
> When true, the sensor will be enabled, rather than disabled.

## Return Values

Returns void

## Examples

```py
MLI.disableSensor('gps')
# When calling gps-related functions, they will behave as if the drone's gps is not present
```
