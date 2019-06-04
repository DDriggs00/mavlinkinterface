# getLeakData()

Reads the data from the leak sensors

## Return Data

Returns a string.  
Returns a JSON string containing data from all

## Examples

getLeakData is called (with a leak near sensor 3) and returns the following JSON

```json
{
    "leakSensor1": 0,
    "leakSensor2": 0,
    "leakSensor3": 1,
    "leakSensor4": 0
}
```
