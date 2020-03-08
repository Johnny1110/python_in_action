import sys
from abc import abstractmethod
from socket import *
from Socket import ProtoData_pb2
from Socket.ProtobufVarint32LengthFieldTools import getBodyLength, encode


class ProtoPySocket:
    def __init__(self, port, host='127.0.0.1'):
        self.HOST = host
        self.PORT = port
        self.ADDR = (self.HOST, self.PORT)
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)

    @abstractmethod
    def processRecord(self, record):
        pass

    def sendRecord(self, record):
        try:
            record_node = record.SerializeToString()
            packet = encode(record_node)
            self.tcpCliSock.send(packet)
        except ConnectionAbortedError:
            print('Connection has been terminated by DMServer on your host.')
            sys.exit(0)

    def processEnd(self):
        try:
            ending_signal = ProtoData_pb2.DMRecord()
            ending_signal.signal = 'close'
            self.sendRecord(ending_signal)
        except ConnectionAbortedError:
            print('Connection has been terminated by DMServer on your host.')
            sys.exit(0)

    def startUp(self):
        try:
            self.tcpCliSock.connect(self.ADDR)
            while True:
                data_len = getBodyLength(self.tcpCliSock)
                protobufdata = self.tcpCliSock.recv(data_len)
                record = ProtoData_pb2.DMRecord()
                record.ParseFromString(protobufdata)
                self.processRecord(record)
                if record.signal.__eq__("close"):
                    break
            self.tcpCliSock.close()
        except ConnectionAbortedError:
            print('Connection has been terminated by DMServer on your host.')
            sys.exit(0)
