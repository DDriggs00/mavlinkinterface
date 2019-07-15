# getAltitude()

Calculates the altitude based on the sonar sensor data.  
Note: Not reliable at short or long range. see official sensor documentation [here](https://bluerobotics.com/store/sensors-sonars-cameras/sonar/ping-sonar-r2-rp/#tab-technical-details)

## Return values

Returns a JSON-Formatted string.  
Upon success, returns the altitude and the confidence  
Upon failure, throws an exception

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
