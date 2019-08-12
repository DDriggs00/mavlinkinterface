# getAltitude()

This function calculates the altitude based on the sonar sensor data.  

Note: Confidence levels are not reliable at short or long range. see official sensor documentation [here](https://bluerobotics.com/store/sensors-sonars-cameras/sonar/ping-sonar-r2-rp/#tab-technical-details)  
Unless future software updates change this, this is not accurate enough to implement terrain following mode.

Note 2: Current sonar software supports only one attached Ping Sonar Sensor.

## Return values

Returns a JSON-Formatted string.  
Upon success, returns the altitude and the confidence  
Upon failure, throws an exception based on the type of error

## Examples

```py
MLI.getAltitude()
```

```json
{
    "altitude":"5.25",
    "confidence":"100"
}
```
