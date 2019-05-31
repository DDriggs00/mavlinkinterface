# cameraPhoto( resolution \<optional>, zoom \<optional>, )
Takes a photo using the camera and returns its path.

## Parameters
resolution (string, optional):  
> Used to reduce the resolution the camera is recording at.  
> Default is 1080p (camera max)

## Return Values
Returns a JSON-formatted string string.  
Upon success, returns the local path of the image.  
Upon failure, returns the reason for failure.

## Examples
```py
cameraPhoto
# Captures a 1080p photo, and returns the following JSON
```
```json
{
    "state":"Success",
    "path":"/.../images/2019-05-22T08.48.34.jpg"
}
```
```py
cameraPhoto(resolution = '720p') 
# takes a 720p photo, but fails due to a lack of storage space and returns the following JSON
```
```json
{
    "state":"Failure",
    "path":null,
    "failReason":"Lack of storage space"
}
```

## Related Mavlink Enumerations

CAMERA_CAP_FLAGS  
CAMERA_ZOOM_TYPE  
SET_FOCUS_TYPE  
CAMERA_MODE
STORAGE_STATUS

## Related Mavlink Functions

MAV_CMD_DO_DIGICAM_CONFIGURE  
MAV_CMD_DO_DIGICAM_CONTROL  
MAV_CMD_DO_SET_CAM_TRIGG_DIST  
MAV_CMD_DO_SET_CAM_TRIGG_INTERVAL  
MAV_CMD_REQUEST_CAMERA_INFORMATION  
MAV_CMD_REQUEST_CAMERA_SETTINGS  
MAV_CMD_REQUEST_STORAGE_INFORMATION  
MAV_CMD_REQUEST_CAMERA_CAPTURE_STATUS  
MAV_CMD_RESET_CAMERA_SETTINGS  
MAV_CMD_SET_CAMERA_MODE  
MAV_CMD_SET_CAMERA_ZOOM  
MAV_CMD_SET_CAMERA_FOCUS  
MAV_CMD_IMAGE_START_CAPTURE  
MAV_CMD_IMAGE_STOP_CAPTURE  
MAV_CMD_REQUEST_CAMERA_IMAGE_CAPTURE (Beta)  
MAV_CMD_DO_TRIGGER_CONTROL  
MAV_CMD_PANORAMA_CREATE