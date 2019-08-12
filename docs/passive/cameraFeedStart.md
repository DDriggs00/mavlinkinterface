# cameraFeedStart()

This command creates and begins streaming a live video stream, returning all data needed to access the stream.

## Return Values

Returns a JSON-formatted string.  
Upon Success, returns all information necessary to access the video stream.  
Upon failure, returns the reason for failure.

## Example

```py
MLI.cameraFeedStart()
# The camera feed is enabled and the following JSON returned
```

## Example Output

```json
{
    "state":"Success",
    "ip":"192.168.2.2",
    "port":"8080"
}
```

## Related Mavlink Commands

- MAV_CMD_DO_CONTROL_VIDEO
- MAV_CMD_VIDEO_START_STREAMING (WIP)  
- MAV_CMD_REQUEST_VIDEO_STREAM_INFORMATION (WIP)  
- MAV_CMD_REQUEST_VIDEO_STREAM_STATUS (WIP)
