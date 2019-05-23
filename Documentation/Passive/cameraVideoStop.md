# cameraVideoStop()
Ends the current video if recording is active

## Return Values
Returns a string.  
Upon Success, Returns "Success"  
Upon Failure, returns failure reason

## Examples
```py
cameraVideoStop # Assuming video is recording
# The currently recording video ends and the video file is finalized, and returns "Success"
cameraVideoStop # Assuming video is not recording
# The currently recording video ends and the video file is finalized, and function returns "Failed, No video to stop"
```