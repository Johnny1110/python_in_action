from Socket.ProtoSocket import ProtoPySocket
from Socket.test import generateTestRecordData


class MyClient(ProtoPySocket):

    def __init__(self, port, host='127.0.0.1'):
        super().__init__(port, host)

    def processRecord(self, record):
        print("收到 record : ")
        print(record)

        if record.signal.__eq__("close"):
            print('通知 server 關閉連接..')
            super(MyClient, self).processEnd()
        else:
            print('嘗試把 record 寫回 server..')
            super(MyClient, self).sendRecord(generateTestRecordData())
            print('---' * 30)




if __name__ == '__main__':
    client = MyClient(host="localhost", port=47596)
    client.startUp()