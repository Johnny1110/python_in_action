import csv

def getTData(fileName):
    Train_Data = []
    with open(fileName, 'r', encoding='utf-8') as file:
        rows = csv.reader(file, delimiter=',')
        for row in rows:
            phoneNum = row[5]  # 取出電話號碼
            staticPhoneNum = row[6]  # 取出座機電話號碼
            addressData = row[7]  # # 取出 Address
            idData = row[1]  # # 取出 ID
            namedData = row[0]  # # 取出 ID

            fakeData0 = generateTrainArray(phoneNum, lable=False)
            fakeData1 = generateTrainArray(staticPhoneNum, lable=False)
            fakeData2 = generateTrainArray(addressData, lable=True)
            fakeData3 = generateTrainArray(idData, lable=False)
            fakeData4 = generateTrainArray(namedData, lable=False)

            Train_Data.append(fakeData0)
            Train_Data.append(fakeData1)
            Train_Data.append(fakeData2)
            Train_Data.append(fakeData3)
            Train_Data.append(fakeData4)

    return Train_Data

def generateTrainArray(text, lable=True):
    data = []
    data.append(text)
    data.append(lable)
    return data


if __name__ == '__main__':
    for data in getTData("data.csv"):
        print(data)