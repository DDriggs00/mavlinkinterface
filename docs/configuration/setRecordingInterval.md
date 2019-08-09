# setRecordingInterval( message, interval )

This function enables, disables, or alters the interval at which data is recorded to a file.

## Parameters

message (string, list):
> The exact name of hte mavlink message to record.  
> If this is a list, the command applies to all listed messages.  

interval (float):
> The number of seconds to wait between data records  
> This has a resolution of 0.5 sec.  
> Set to 0 to log every message.  
> Set to -1 to disable logging.

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
