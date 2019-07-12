import socket                   # For communicating via udp
import json                     # For formatting output
from brping import pingmessage  # For communication with the sensor


# Repurposed from code found here:
# https://discuss.bluerobotics.com/t/4397/13
class sonar(object):
    def __init__(self):
        # set address
        self.address = ("192.168.2.2", 9090)

        # Configure Socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.settimeout(1.0)

        # create pingmessage parser
        self.__parser = pingmessage.PingParser()

    def __request(self, id):
        '''
        Request new messages of a specific ID

        :param id: The ID to refrest messages with
        '''
        msg = pingmessage.PingMessage()
        msg.request_id = id
        msg.pack_msg_data()
        self.__sock.sendto(msg.msg_data, self.address)

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
        self.__request(message)
        try:
            data, addr = self.__sock.recvfrom(1024)
        except socket.timeout:  # If unable to retrieve the requested data within 1 sec
            return "{'Error': 'Timeout when retrieving message'}"

        parsedData = self.__parse(data)

        # Convert specialized object to dictionary
        returnDict = {}
        for field in pingmessage.payload_dict[parsedData.message_id]['field_names']:
            returnDict[field] = str(getattr(parsedData, field))

        return json.dumps(returnDict)
