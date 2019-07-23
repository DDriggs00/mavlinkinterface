# GetTemperature()

Gets the coordinates from the GPS unit  
Coordinates will only be returned if a GPS Lock is present.

## Return Values

Returns a string.  
If a gps lock is present, returns the current coordinates (lat/lon only)  
If no lock was present, throws a ConnectionError

### example output (expanded)

```json
{
    "lat": 33.810313,
    "lon": -118.393867
}
```

## Examples

```py
try:
    coordinates = MLI.gps.getCoordinates()  # Get Coordinates
    coordinateDict = json.loads(coords)     # Convert JSON to dict
    print('latitude: ' + coordinateDict['lat'])
    print('longitude: ' + coordinateDict['lon'])
except ConnectionError: # Catch exception thrown if lock is not present
    print('GPS does not have lock')
```
