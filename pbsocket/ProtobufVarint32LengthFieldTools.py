import sys
import bitstring

def computeReadableRawSize(head_array):
    readable_length_array = []
    for index, data in enumerate(head_array):
        temp = int.from_bytes(data, byteorder='big', signed=False)
        if int.from_bytes(data, byteorder='big', signed=True) < 0:
            temp ^= 0x80  # 若 bin 開頭為 1 就換成 0
        temp <<= (index * 7)
        readable_length_array.append(temp)

    readable_length = 0
    for data in readable_length_array:
        readable_length += data

    return readable_length


def getBodyLength(tcpCliSock):
    readable_length = 0
    head_array = []

    for i in range(1, 6):
        try:
            head_data = tcpCliSock.recv(1)  # 收標頭
            head_array.append(head_data)
            if int.from_bytes(head_data, byteorder='big', signed=True) >= 0:
                readable_length = computeReadableRawSize(head_array)
                break
        except ConnectionResetError:
            print('Connection has been terminated by DMServer on your host.')
            sys.exit(0)

    return readable_length

def writeRawVarint32Header(stream, bodyLen):
    while True:
        if bodyLen & ~0x7F == 0:
            stream.append(int.to_bytes(bodyLen, length=1, byteorder='big'))
            break
        else:
            stream.append(int.to_bytes((bodyLen & 0x7F) | 0x80, length=1, byteorder='big'))
            bodyLen >>= 7


def frameDecoder(tcpCliSock):
    data_len = getBodyLength(tcpCliSock)
    return tcpCliSock.recv(data_len)

def frameEncoder(record_bytes):
    bodyLen = len(record_bytes)
    # headerLen = computeRawVarint32Size(bodyLen)
    stream = bitstring.BitStream()
    writeRawVarint32Header(stream, bodyLen)
    stream.append(record_bytes)
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
    # length = 0b1111010000000011
    # print(length.to_bytes(2, byteorder='big', signed=False))
    test_header_array = [b'\xf4', b'\x03']
    length = computeReadableRawSize(test_header_array)
    print("length : ", length)