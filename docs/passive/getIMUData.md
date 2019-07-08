# getIMUData()

Combines the outputs of getAccelerometerData(), getGyroscopeData(), and getMagnetometerData().

## Return Values

Returns a JSON-formatted string.  
Returns Accelerometer, Gyroscope, and Magnetometer data.

## Example output

```json
{
    "accelerometer": {
        "X":1.25,
        "Y":-4.3,
        "Z":-9.81
    },
    "gyroscope": {
        "X":90,
        "Y":1.25,
        "Z":-3.9
    },
    "magnetometer":{
        "X":-123.45,
        "Y":12.5,
        "Z":50.1
    }
}
```
