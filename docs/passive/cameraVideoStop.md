# cameraVideoStop()

Ends the current video if recording is active

## Return Values

Returns a string.  
Upon Success, Returns "Success"  
Upon Failure, returns failure reason

## Examples

```py
MLI.cameraVideoStop() # Assuming video is recording
# The currently recording video ends and the video file is finalized, and returns "Success"

MLI.cameraVideoStop() # Assuming video is not recording
# The currently recording video ends and the video file is finalized, and function returns "Failed, No video to stop"
```

## Related Mavlink Commands

- MAV_CMD_DO_CONTROL_VIDEO  
- MAV_CMD_REQUEST_STORAGE_INFORMATION  
- MAV_CMD_VIDEO_STOP_CAPTURE  
