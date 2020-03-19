from pbsocket import PbClientSocket


class MyClient(PbClientSocket):
    def processRecord(self, record):
        print(record)
        print('---'*30)
        self.sendRecord(record)
        if record.signal.__eq__(record.Signal.STOP):
            self.processEnd()

if __name__ == '__main__':
    myClient = MyClient()
    myClient.startUp()