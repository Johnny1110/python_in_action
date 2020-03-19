import sys
from abc import abstractmethod
from socket import *

from pbsocket import ProtoData_pb2
from pbsocket.ProtobufVarint32LengthFieldTools import frameDecoder, frameEncoder


class PbClientSocket:

    def __init__(self, host='127.0.0.1', port=8080):
        self.ADDR = (host, port)
        self.tcpCliSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET 是使用 IPv4 協定，SOCK_STREAM 是使用 TCP 協定


    @abstractmethod
    def processRecord(self, record):
        pass


    def sendRecord(self, record):
        try:
            record_node = record.SerializeToString()
            frame = frameEncoder(record_node)
            self.tcpCliSocket.send(frame)
        except ConnectionAbortedError:
            print('Connection has been terminated by DMServer on your host.')
            sys.exit(0)

    def processEnd(self):
        try:
            ending_signal = ProtoData_pb2.Record()
            ending_signal.signal = ending_signal.Signal.STOP
            self.sendRecord(ending_signal)
        except ConnectionAbortedError:
            print('Connection has been terminated by DMServer on your host.')
            sys.exit(0)

    def startUp(self):
        try:
            self.tcpCliSocket.connect(self.ADDR)
            while True:
                protobufdata = frameDecoder(self.tcpCliSocket)
                record = ProtoData_pb2.Record()
                record.ParseFromString(protobufdata)
                self.processRecord(record)
                if record.signal.__eq__(record.Signal.STOP):
                    break
            self.tcpCliSocket.close()
        except ConnectionAbortedError:
            print('Connection has been terminated by DMServer on your host.')
            sys.exit(0)