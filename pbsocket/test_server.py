from pbsocket import ProtoData_pb2, PbServerSocket

if __name__ == '__main__':
    data1 = ProtoData_pb2.PbData()
    data1.dataType = data1.DataType.STRING
    data1.binaryData = "Hello Wolrd!".encode('utf-8')
    data2 = ProtoData_pb2.PbData()
    data2.dataType = data2.DataType.INT
    data2.binaryData = int(21).to_bytes(4, byteorder='big')
    record = ProtoData_pb2.Record()
    record.signal = record.Signal.NODE
    record.column['msg'].CopyFrom(data1)
    record.column['age'].CopyFrom(data2)

    recordEnd = ProtoData_pb2.Record()
    recordEnd.signal = record.Signal.STOP

    server = PbServerSocket()
    server.record_list.append(record)
    # server.record_list.append(recordEnd)
    server.startUp()

