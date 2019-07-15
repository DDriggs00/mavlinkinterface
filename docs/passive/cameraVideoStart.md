# cameraVideoStart( time \<optional>, resolution \<optional> )

Starts the camera recording video. The video will end when either the cameraVideoStop is called, the optional timer ends, or the internal storage runs out.

## Parameters

time (integer, optional):  
> The number of seconds to record video before automatically ending

resolution (string, optional):  
> Used to reduce the resolution the camera is recording at.  
> Default is 1080p (camera max)

## Return Values

Returns a JSON-formatted string string.  
Upon success, returns the local path of the video.  
Upon failure, returns the reason for failure.

## Examples

```py
MLI.cameraVideoStart()
# Starts the video feed to record until stopped at 1080p, returns the following JSON
```

```json
{
    "state":"Success",
    "path":"/.../video/2019-05-22T08.48.34.mp4"
}
```

```py
MLI.cameraVideoStart(time = 3600, resolution = '720p')
# Starts the video feed to record for up to 1 hour at 720p, but fails due to a lack of storage space and returns the following JSON
```

```json
{
    "state":"Failure",
    "path":"/.../video/2019-05-22T09.48.34.mp4",
    "failReason":"Lack of storage space"
}
```

## Related Mavlink Commands

- MAV_CMD_DO_CONTROL_VIDEO  
- MAV_CMD_REQUEST_STORAGE_INFORMATION  
- MAV_CMD_VIDEO_START_CAPTURE
