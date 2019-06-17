# import json
from configparser import ConfigParser

config = ConfigParser()
config.read("mavlinkinterface/config.cfg")
surfacePressure = int(config['geodata']['surfacePressure'])     # pascals
fluidDensity = int(config['geodata']['fluidDensity'])           # kg/m^3
g = 9.8066                                                      # m/s^2

def getPressureExternal(ml):
    ''' Returns the reading of the pressure sensor in Pascals '''
    pressure_data = ml.recv_match(type="SCALED_PRESSURE", blocking=True)   # Pressure is in millibars by default
    return round(100 * float(pressure_data.press_abs), 2)   # convert to Pascals before returning

def getDepth(ml):
    '''Returns the depth of the drone in meters'''
    depth = ((getPressureExternal(ml) - surfacePressure) / (fluidDensity * g)) * -1
    return round(depth, 2)    # meters
