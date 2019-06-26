from threading import Thread, Event
from time import sleep

class test(object):
    def __init__(self):
        self.a = 1
        self.b = 2

    def x(self):
        while not self.killer.is_set():
            print("a")
            sleep(1)
            print("b")
            sleep(1)

    def start(self):
        self.killer = Event()
        self.leakDetectorThread = Thread(target=self.x)
        self.leakDetectorThread.daemon = True
        self.leakDetectorThread.start()


test = mli.mavlinkConnection.recv_msg()
test.get_fieldnames()
test.get_type()

test2 = mli.mavlinkConnection.recv_match(type="HEARTBEAT")
mavutil.mavlink.enums['MAV_TYPE'][test2.type].name
mavutil.mavlink.enums['MAV_AUTOPILOT'][test2.autopilot].name

logString = "SCALED_PRESSURE2"
fields = mli.messages["SCALED_PRESSURE2"].get_fieldnames()
for field in fields:
    logString += ", " + mli.messages["SCALED_PRESSURE2"].str(field)


logMessages = ["SYS_STATUS", 'RAW_IMU', 'SCALED_PRESSURE2', 'HEARTBEAT', 'ATTITUDE']
logMessages2 = "SYS_STATUS, RAW_IMU, SCALED_PRESSURE2, HEARTBEAT, ATTITUDE"

msg = mli.mavlinkConnection.recv_match(type=logMessages, blocking=True, timeout=1)

# temp = mli.mavlinkConnection.recv_match(type="ATTITUDE", blocking=True)
# temp = '{' + str(temp).split('{', 1)[1]
# json.loads(sub('(\w+)\s?:\s?("?[^",]+"?,?)', "\"\g<1>\":\g<2>", temp))
