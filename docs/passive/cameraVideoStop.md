# cameraVideoStop()

This function stops and finalizes any recording videos.

## Return Values

Returns void.  
Upon Failure, throws a FileError

## Examples

```py
MLI.cameraVideoStop() # Assuming video is recording
# The currently recording video ends and the video file is finalized.

MLI.cameraVideoStop() # Assuming video is not recording
# The currently recording video ends and the video file is finalized, and function throws a fileError
```

## Related Mavlink Commands

- MAV_CMD_DO_CONTROL_VIDEO  
- MAV_CMD_REQUEST_STORAGE_INFORMATION  
- MAV_CMD_VIDEO_STOP_CAPTURE  
