import json
from collections import namedtuple

from TODO.typesetting.tools import RowSetInfo

tabCount = 4

encode = "ms950"

data = [
    {
        "id": "321",
        "name": "Johnny Wang",
        "愛好": '滑雪',
        "地址": "台北市大安區新生南路一段143巷34號",
        "skills": ['Java', 'python', 'JS']
    },
    {
        "id": "438",
        "name": "Ben Lee",
        "愛好": ['唱歌', '跳舞', '洗澡', '看電影'],
        "地址": "高雄市左營區新下街56號",
        "skills": ['唱歌', '跳舞']
    },
{
        "id": "438",
        "name": "Ben Lee",
        "愛好": ['唱歌', '跳舞', '洗澡', '看電影'],
        "地址": "高雄市左營區新下街56號",
        "skills": ['跳舞']
    },
]


def extractColumnName(row):
    return [key for key in row]


def caculatecolumnMaxLength(columnNames, data):
    resultMap = {}
    for name in columnNames:
        resultMap[name] = 0

    for row in data:
        for name in columnNames:
            if row[name].__class__ is [].__class__:  # 如果是陣列的話
                rowList = row[name]
                for text in rowList:
                    encodedText = text.encode(encode)
                    if len(encodedText) > resultMap[name]:
                        resultMap[name] = len(encodedText)
            else:
                encodedText = row[name].encode(encode)
                if len(encodedText) > resultMap[name]:
                    resultMap[name] = len(encodedText)
    print("[INFO]: 各欄位所需半型長度: ", resultMap)
    return resultMap


def caculateColumnNeededSpace(data):
    columnNames = extractColumnName(data[0])
    columnMaxLength = caculatecolumnMaxLength(columnNames, data)
    return columnMaxLength


def writeColumnNames(columnMaxLength, file):
    for key in columnMaxLength:
        encodedKey = key.encode(encode)
        padding = columnMaxLength[key] - len(encodedKey)
        file.write(key)
        # file.write("　" * int(padding / 2))
        # file.write(" " * int(padding % 2))
        file.write(" " * padding)
        file.write("\t"*tabCount)
    file.write("\n")


def writeFirstOneOfDataList(maxLength, text, io):
    encodedText = text.encode(encode)
    padding = maxLength - len(encodedText)
    io.write(text)
    # io.write("　" * int(padding / 2))
    # io.write(" " * int(padding % 2))
    io.write(" " * padding)
    io.write("\t"*tabCount)


def processRowDataList(maxLength, columnName, dataList, io, rowSetInfo):
    dataCount = len(dataList)
    writeFirstOneOfDataList(maxLength, dataList[0], io)
    restData = dataList[1:]
    if len(restData) != 0:
        rowSetInfo.addRestData(columnName, restData)


def processRestRowData(rowSetInfo, columnMaxLength, io):
    while True:
        theData = rowSetInfo.popWritableData()

        if theData is None:
            break

        for key in columnMaxLength:
            if theData.__contains__(key):
                text = theData[key]
                encodedText = text.encode(encode)
                padding = len(encodedText) - columnMaxLength[key]
                io.write(text)
                # io.write("　" * int(padding / 2))
                # io.write(" " * int(padding % 2))
                io.write(" " * padding)
                io.write("\t" * tabCount)
            else:
                padding = columnMaxLength[key]
                # io.write("　" * int(padding / 2))
                # io.write(" " * int(padding % 2))
                io.write(" " * padding)
                io.write("\t" * tabCount)
        io.write("\n")



def startWriteData(columnMaxLength, data):
    with open('test.txt', mode='a', encoding='utf-8') as file:
        writeColumnNames(columnMaxLength, file)  # 先寫入欄位名稱

        for row in data:
            rowSetInfo = RowSetInfo()
            for columnName in columnMaxLength:
                rowData = row[columnName]
                if rowData.__class__ is [].__class__:  # rowData 做陣列處裡
                    processRowDataList(maxLength=columnMaxLength[columnName], columnName=columnName, dataList=rowData, io=file, rowSetInfo=rowSetInfo)
                else:  # rowData 為一般文字資料
                    padding = columnMaxLength[columnName] - len(rowData.encode(encode))  # 計算留白空間
                    file.write(rowData)
                    # file.write("　" * int(padding / 2))
                    # file.write(" " * int(padding % 2))
                    file.write(" " * padding)
                    file.write("\t"*tabCount)

            file.write("\n")
            processRestRowData(rowSetInfo, columnMaxLength, file)


def processData(data):
    columnMaxLength = caculateColumnNeededSpace(data)
    startWriteData(columnMaxLength, data)

if __name__ == '__main__':
    with open("test.json", mode='r', encoding='utf-8') as dataFile:
        data_str = dataFile.read()
        data = json.loads(data_str, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        python_array = []
        for d in data:
            rowData = json.loads(d)
            python_array.append(rowData)

        processData(python_array)