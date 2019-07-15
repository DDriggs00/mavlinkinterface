# setRecordingInterval( sensor, interval )

Set how long to wait between recording data on the given sensor to a file.  
NOTE: the sensors only send messages at a rate of 4 hz, so any logging more frequent than that would be wasted

## Parameters

sensor (string, list):
> The sensor to log.  
> If this is a list, the command applies to all listed sensors.  
> To configure all sensors at once, set this to "All"

interval (float):
> The number of seconds to wait between data records  
> Set to 0 to disable logging

## Return Values

Returns void

## Examples

```py
MLI.setRecordingInterval( "Depth", 10 )
# The depth sensor will now be recorded every 10 seconds

MLI.setRecordingInterval( ["Depth", "Temperature", "Magnetometer"], 0 )
# The Depth sensor, Temperature, and magnetometer will not be logged

MLI.setRecordingInterval( "All", .25 )
# All available sensors will be logged 4 times per second
```
