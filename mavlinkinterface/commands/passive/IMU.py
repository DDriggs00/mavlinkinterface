import json

def getMagnetometerData(ml):
    imu = ml.recv_match(type="RAW_IMU", blocking=True)
    data = {}
    data['X'] = imu.xmag
    data['Y'] = imu.ymag
    data['Z'] = imu.zmag
    return json.dumps(data)

def getAccelerometerData(ml):
    imu = ml.recv_match(type="RAW_IMU", blocking=True)
    data = {}
    data['X'] = imu.xacc
    data['Y'] = imu.yacc
    data['Z'] = imu.zacc
    return json.dumps(data)

def getGyroscopeData(ml):
    imu = ml.recv_match(type="RAW_IMU", blocking=True)
    data = {}
    data['X'] = imu.xgyro
    data['Y'] = imu.ygyro
    data['Z'] = imu.zgyro
    return json.dumps(data)

def getIMUData(ml):
    data = {}
    data["Magnetometer"] = json.loads(getMagnetometerData(ml))
    data["Accelerometer"] = json.loads(getAccelerometerData(ml))
    data["Gyroscope"] = json.loads(getGyroscopeData(ml))
    return json.dumps(data)
