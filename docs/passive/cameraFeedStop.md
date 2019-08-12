# cameraFeedStop()

This command stops any ongoing video feeds.

## Return Values

Returns void.  
Upon failure, throws an exception.

## Examples

```py
MLI.cameraFeedStop()
# The camera feed is ended
```

## Related Mavlink Commands

- MAV_CMD_DO_CONTROL_VIDEO
- MAV_CMD_VIDEO_STOP_STREAMING (WIP)  
- MAV_CMD_REQUEST_VIDEO_STREAM_INFORMATION (WIP)  
- MAV_CMD_REQUEST_VIDEO_STREAM_STATUS (WIP)
