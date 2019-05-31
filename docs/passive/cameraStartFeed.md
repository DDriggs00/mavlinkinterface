# cameraStartFeed()
Creates a camera feed that the controller can access.

## Return Values
Returns a JSON-formatted string.  
Upon Success, returns all information necessary to access the video stream.  
Upon failure, returns the reason for failure.

## Examples
```py
cameraStartFeed
# The camera feed is enabled and the following JSON returned
```
```json
{
    "state":"Success",
    "ip":"Stream IP",
    "port":"Stream Port"
    ...
}
```