# setRecordingInterval( sensor, interval )

Set how long to wait between recording data on the given sensor to a file.  
NOTE: the sensors only send messages at a rate of 4 hz, so any logging more frequent than that would be wasted

## Parameters

sensor (string, list):
> The sensor to log.  
> If this is a list, the command applies to all listed sensors.  

interval (float):
> The number of seconds to wait between data records  
> Set to 0 to log every message
> Set to -1 to disable logging

## Return Values

Returns void

## Examples

```py
MLI.setRecordingInterval( "SCALED_PRESSURE2", 10 )
# The depth sensor will now be recorded every 10 seconds

MLI.setRecordingInterval( ["SCALED_PRESSURE2", "RAW_IMU", "ATTITUDE"], 0 )
# The Depth sensor, IMU, and attitude will have every message logged

MLI.setRecordingInterval( ["SCALED_PRESSURE2", "RAW_IMU", "ATTITUDE"], -1 )
# The Depth sensor, IMU, and attitude will not be logged
```
