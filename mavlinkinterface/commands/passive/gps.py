import json
from datetime import datetime


class gps(object):
    def __init__(self, mli):
        self.mli = mli
        pass

    def getCoordinates(self) -> str:
        if ((datetime.now() - self.mli.messages['GPS_RAW_INT']['time']).total_seconds() < 1 and
                (self.mli.messages['GPS_RAW_INT']['message'].fix_type >= 2)):
            returnObj = {}
            returnObj['lat'] = self.mli.messages['GPS_RAW_INT']['message'].lat * 1e-7
            returnObj['lon'] = self.mli.messages['GPS_RAW_INT']['message'].lon * 1e-7
            return json.dumps(returnObj)
        else:
            raise ConnectionError("Could not get GPS Data")

    def setWaypoint(self):
        pass

    def goToWaypoint(self, lat, lon, acceptRadius, passRadius, ):
        pass

    def loiter(self, lat: float, lon: float, radius: float = 1, yaw: float = None, type: str = 'unlimited', n: float = -1):
        pass

    def orbit(self, lat: float, lon: float, radius: float = 1, speed: float = 1, yaw: int = 1):
        pass

    def pathPlanning(self,
                     targetLat: float,
                     targetLon: float,
                     targetYaw: float,
                     localPathPlanning: int,
                     fullPathPlanning: int):
        pass
    
    def navSpline(self, lat: float, lon: float, hold: int):
        pass

    def delay(self, tine, h: int = None, m: int = None, s: int = None):
        pass

    def yaw(self, angle: float, speed: float, direction: bool, absolute: bool):
        pass

    def changeSpeed(self, speedType: int, speed: float, throttle: int, absolute: bool):
        pass

    def setHome(self, lat: float = None, lon: float = None):
        '''
        Sets the GPS Home position to the given coordinates (or the current position if none are given)

        :param lat: the latitude to set as home in decimal degrees (use at least 6 decimal places)
        :param lon: the longitude to set as home in decimal degrees (use at least 6 decimal places)
        Note: if either lat or lon is present, both must be present
        '''

        if lat is None and lon is None:
            pass    # TODO
        elif lat is not None and lon is not None:
            pass    # TODO
        else:
            print("Coordinates may only be passed in pairs")

        self.log.debug('Setting Home to ' + str(lat) + ', ' + str(lon))

    def goToHome(self):
        pass

    def pauseContinue(self, pause: bool):
        pass

    def enableFence(self, enable: bool):
        pass

    def setYawSpeed(self, angle: float, speed: float, absolute: bool):
        pass

    def terminate(self):
        pass

    def startMission(self, first: int, last: int):
        pass
