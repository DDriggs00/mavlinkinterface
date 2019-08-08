# External
import socket                   # For communicating via udp
import json                     # For formatting output
from brping import pingmessage  # For communication with the sensor
# Internal
from mavlinkinterface.logger import getLogger   # For logging


# Repurposed from code found here:
# https://discuss.bluerobotics.com/t/4397/13
class sonar(object):
    def __init__(self):

        self.disabled = False
        self.log = getLogger('sonar')
        self.log.trace('Sonar sensor initialization started')
        # set address
        self.address = ("192.168.2.2", 9090)

        # Configure Socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.settimeout(1.0)

        # create pingmessage parser
        self.__parser = pingmessage.PingParser()
        self.log.trace('Sonar sensor initialization completed')
        self.log.trace('Note that this does not guarantee a working sonar sensor is attached')

    def __request(self, id):
        '''
        Request new messages of a specific ID

        :param id: The ID to refrest messages with
        '''
        msg = pingmessage.PingMessage()
        msg.request_id = id
        msg.pack_msg_data()
        self.__sock.sendto(msg.msg_data, self.address)
        self.log.trace('Request sent for message of id: ' + str(id))

    # parse data to create ping messages
    def __parse(self, data):
        '''
        Parses the given data

        :param data: the data to parse
        '''
        for b in bytearray(data):
            if self.__parser.parse_byte(b) == self.__parser.NEW_MESSAGE:
                return self.__parser.rx_msg
        return {}   # If message is empty

    def getMessage(self, message=pingmessage.PING1D_DISTANCE_SIMPLE):
        '''
        Requests and retrieves the given message from the sonar sensor
        For a list of messages and what they return, check here:
        https://docs.bluerobotics.com/ping-protocol/pingmessage-ping1d/
        '''
        self.log.trace('Getting sonar message of id: ' + str(message))
        self.__request(message)
        try:
            if self.disabled:
                raise socket.timeout
            data, addr = self.__sock.recvfrom(1024)
        except socket.timeout:  # If unable to retrieve the requested data within 1 sec
            self.log.error('A Timeout occurred when retrieving a sonar message of id ' + str(message))
            raise TimeoutError('A Timeout occurred when retrieving a sonar message of id ' + str(message))

        parsedData = self.__parse(data)

        # Convert specialized object to dictionary
        returnDict = {}
        for field in pingmessage.payload_dict[parsedData.message_id]['field_names']:
            returnDict[field] = str(getattr(parsedData, field))
        returnJson = json.dumps(returnDict)
        self.log.trace('getMessage preparing to return ' + returnJson)
        return returnJson
