# GetBatteryData()

Reads battery statistics and calculates battery percentage

## Return Values

Returns a JSON-Formatted string.  
Returns all available information about the battery.

## Examples

Example output:

```json
{
    "voltage":12.3,
    "currentDraw":1.2,
    "percentRemaining":72.5
}
```

## Related Mavlink Enumerations

- [MAV_BATTERY_TYPE](https://mavlink.io/en/messages/common.html#MAV_BATTERY_TYPE)
- [MAV_BATTERY_FUNCTION](https://mavlink.io/en/messages/common.html#MAV_BATTERY_FUNCTION)
- [MAV_BATTERY_CHARGE_STATE](https://mavlink.io/en/messages/common.html#MAV_BATTERY_CHARGE_STATE)
- [MAV_SMART_BATTERY_FAULT](https://mavlink.io/en/messages/common.html#MAV_SMART_BATTERY_FAULT)

## Related Mavlink Functions

- [BATTERY_STATUS](https://mavlink.io/en/messages/common.html#BATTERY_STATUS)
- [SMART_BATTERY_INFO](https://mavlink.io/en/messages/common.html#SMART_BATTERY_INFO) (Beta)
- [SMART_BATTERY_STATUS](https://mavlink.io/en/messages/common.html#SMART_BATTERY_STATUS) (Beta)
