import sys

from Socket.ProtoException import CorruptedFrameException
import bitstring

def readRawVarint32(head_array):
    temp = b''
    for i in head_array:
        temp += i
    return int.from_bytes(temp, byteorder='big')


def getBodyLength(tcpCliSock):
    data_len = 0
    head_array = []

    for i in range(1, 6):
        try:
            head_data = tcpCliSock.recv(1)  # 收標頭
            head_array.append(head_data)
            if(int.from_bytes(head_data, byteorder='big', signed=True) >= 0):
                data_len = readRawVarint32(head_array)
                if data_len < 0:
                    raise CorruptedFrameException("negative length: " + data_len)
                else:
                    break
        except ConnectionResetError:
            print('Connection has been terminated by DMServer on your host.')
            sys.exit(0)

    return data_len


def writeRawVarint32Header(stream, bodyLen):
    while True:
        if bodyLen & ~0x7F == 0:
            stream.append(int.to_bytes(bodyLen, length=1, byteorder='big'))
            break
        else:
            stream.append(int.to_bytes((bodyLen & 0x7F) | 0x80, length=1, byteorder='big'))
            bodyLen >>= 7


def encode(record_bytes):
    bodyLen = len(record_bytes)
    headerLen = computeRawVarint32Size(bodyLen)
    print("header_length : ", headerLen)
    print('body_length : ', bodyLen)
    stream = bitstring.BitStream()
    print('stream_length : ', stream.len)
    writeRawVarint32Header(stream, bodyLen)
    stream.append(record_bytes)
    print(stream)
    print(stream.bin)
    return stream.tobytes()



def computeRawVarint32Size(data_length):
    if (data_length & (0xffffffff << 7)) == 0:
        return 1
    if (data_length & (0xffffffff << 14)) == 0:
        return 2
    if (data_length & (0xffffffff << 21)) == 0:
        return 3
    if (data_length & (0xffffffff << 28)) == 0:
        return 4
    return 5


if __name__ == '__main__':
    data = '你好阿，~XD!你好阿，~XD!你好阿，~XD!你好阿，~XD!你好阿，~XD!你好阿，~XD!你好阿，~XD!'.encode('utf-8')
    print('data : ', data)
    packet = encode(data)
    print("解析封包長度 : ", packet)
    print(packet[0])
