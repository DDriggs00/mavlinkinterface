# arm()
Enables the propellers if the pre-arm safety checks pass. 

## Return Values
Returns a string.  
Upon success or failure, returns the success/fail status, and each of the pre-arm safety checks, their pass/fail status, and their return values

## Example
arm command is run and fails, output:
```json
{
    "state":"Success",
    "checks": {
        "check1": {
            "state":"Pass",
            "output": 1234
        },
        "check2": {
            "state":"Fail",
            "output": 1234
        },
        "check3": {
            "state":"Pass",
            "output": false
        }
    }
}
```

## Related Mavlink Enumerations

- [MAV_ARM_AUTH_DENIED_REASON](https://mavlink.io/en/messages/common.html#MAV_ARM_AUTH_DENIED_REASON)

## Related Mavlink Functions

- [MAV_CMD_COMPONENT_ARM_DISARM](https://mavlink.io/en/messages/common.html#MAV_CMD_COMPONENT_ARM_DISARM)
- [MAV_CMD_ARM_AUTHORIZATION_REQUEST](https://mavlink.io/en/messages/common.html#MAV_CMD_ARM_AUTHORIZATION_REQUEST)