# getAllSensorData()

This function gets all data from all sensors, and returns in as a JSON.

## Return Values

Returns a JSON-formatted string.  
Returns all data from every currently-attached sensor.  
For individual sensor formatting, see each sensor's command's documentation

## Example Output

```json
{
    "accelerometer": {
        "X":1.25,
        "Y":-4.3,
        "Z":-9.81
    },
    "Battery":{
        "voltage":12.3,
        "currentDraw":1.2,
        "percentRemaining":72.5
    },
    "Heading":270,
    "Depth": 2.6,
    "Gyroscope": {
        "Axis-1":90,
        "Axis-2":1.25,
        "Axis-3":-3.9
    },
    "leak": {
        "leakSensor1": 0,
        "leakSensor2": 0,
        "leakSensor3": 1,
        "leakSensor4": 0
    },
    "Magnetometer":{
        "X":-123.45,
        "Y":12.5,
        "Z":50.1
    },
    "PressureInternal": 100.5,
    "PressureExternal": 100.5,
    "Temperature": 30.4,
    "Sonar":"whatever the Sonar returns"
}
```
