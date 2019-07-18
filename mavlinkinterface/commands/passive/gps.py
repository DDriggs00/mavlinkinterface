import json
from datetime import datetime


class gps(object):
    def __init__(self, mli):
        self.mli = mli
        pass

    def getCoordinates(self) -> str:
        '''Returns the current coordinates of the drone, throws an exception if no lock is available'''
        if ((datetime.now() - self.mli.messages['GPS_RAW_INT']['time']).total_seconds() < 1 and
                (self.mli.messages['GPS_RAW_INT']['message'].fix_type >= 2)):

            returnObj = {}
            returnObj['lat'] = self.mli.messages['GPS_RAW_INT']['message'].lat * 1e-7
            returnObj['lon'] = self.mli.messages['GPS_RAW_INT']['message'].lon * 1e-7
            return json.dumps(returnObj)
        else:
            raise ConnectionError("Could not get GPS Data")
