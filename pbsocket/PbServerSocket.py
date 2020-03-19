import threading

from socket import *
from pbsocket import ProtoData_pb2
from pbsocket.ProtobufVarint32LengthFieldTools import frameEncoder, frameDecoder


class PbServerSocket:

    def __init__(self, record_list=[], host='127.0.0.1', port=8080):
        self.alive = False
        self.output_list = []
        self.record_list = record_list
        self.ADDR = (host, port)
        self.tcpServSocket = socket(AF_INET, SOCK_STREAM) # AF_INET 是使用 IPv4 協定，SOCK_STREAM 是使用 TCP 協定

    def sendRecord(self, conn):
        for record in self.record_list:
            binData = record.SerializeToString()  # 把 record 序列化成 bytes
            binData = frameEncoder(binData)  # 把 bytes_record 轉化為 varint32 訊框
            conn.send(binData)

    def recvRecord(self, conn, addr):
        while True:
            protobufdata = frameDecoder(conn)  # 解碼第一筆資料
            record = ProtoData_pb2.Record()
            record.ParseFromString(protobufdata)  # bytes 轉碼變 ProtoBuf 物件
            if record.signal.__eq__(record.Signal.NODE):
                self.output_list.append(record)
                print(record)
                continue
            if record.signal.__eq__(record.Signal.STOP):
                print('data transfrom already finished, close the connection : ', addr)
                conn.close()
                break

    def processConn(self, conn, addr):
        recordSender = threading.Thread(target=self.sendRecord, args=(conn,))
        recordRecver = threading.Thread(target=self.recvRecord, args=(conn, addr,))
        recordSender.start()
        recordRecver.start()

    def close(self):
        self.alive = False

    def startUp(self):
        self.alive = True
        self.tcpServSocket.bind(self.ADDR)
        self.tcpServSocket.listen(5)
        print('tcpServSocket start up successfully, server info : ', self.ADDR)
        while self.alive:
            conn, addr = self.tcpServSocket.accept()
            print('accepted connection from : ', addr)
            self.processConn(conn, addr)




