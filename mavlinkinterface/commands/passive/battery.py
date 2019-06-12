import json

def getBatteryData(ml):
    sysStatus = ml.recv_match(type="SYS_STATUS")
    data = {}
    data['voltage'] = sysStatus.voltage_battery / 1000
    data['current'] = sysStatus.current_battery
    data['percent_remaining'] = sysStatus.battery_remaining
    return json.dumps(data)