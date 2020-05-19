import csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

dict_map = {'0': 1, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, '6': 7, '7': 8, '8': 9, '9': 10, '(': 11, ')': 12, '-': 13, ' ': 14, '#': 15}

def getTData(fileName):
    Train_Data = []
    with open(fileName, 'r', encoding='utf-8') as file:
        rows = csv.reader(file, delimiter=',')
        for row in rows:
            phoneNum = row[5]  # 取出電話號碼 (正確資料)
            staticPhoneNum = row[6]  # 取出座機電話號碼 (錯誤資料)
            addressData = row[7]  # # 取出 Address (錯誤資料)
            idData = row[1]  # # 取出 ID (錯誤資料)
            namedData = row[0]  # # 取出 ID (錯誤資料)

            trueData = generateTrainArray(phoneNum, lable=False)
            fakeData1 = generateTrainArray(staticPhoneNum, lable=True)
            fakeData2 = generateTrainArray(addressData, lable=False)
            fakeData3 = generateTrainArray(idData, lable=False)
            fakeData4 = generateTrainArray(namedData, lable=False)


            Train_Data.append(trueData)
            Train_Data.append(fakeData1)
            Train_Data.append(fakeData2)
            Train_Data.append(fakeData3)
            Train_Data.append(fakeData4)

    return Train_Data


def generateTrainArray(text, lable=True):
    word_length = len(text)
    buffer = [0 for i in range(14)]  # 建立陣列

    for i in range(word_length):
        if i > 11:
            break

        # 先使用字典映射 phoneNum
        try:
            mapped_word = dict_map[text[i]]
            buffer[i] = mapped_word
        except:
            buffer[i] = 0

    buffer[12] = word_length  # 第 12 欄加入號碼長度
    buffer[13] = int(lable)  # 第 12 欄加入號碼長度
    return buffer


def start():
    Trian_Data = getTData("data.csv")
    df = pd.DataFrame(Trian_Data)
    print(df)

    # 將資料分成訓練組及測試組
    # 因為 index(13) 是之後要預測的變數，所以X軸不用
    X = df.drop(13, axis=1)
    print(X)
    y = df[13]
    print(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    # 使用隨機森林與決策樹做比較
    # n_estimator代表要使用多少CART樹（CART樹為使用GINI算法的決策樹）
    rfc = RandomForestClassifier(n_estimators=200)

    # 從訓練組資料中建立隨機森林模型
    rfc.fit(X_train, y_train)

    # 預測測試組的電話號碼是否發生
    rfc_pred = rfc.predict(X_test)
    print(rfc_pred)

    # 利用confusion_matrix來看實際及預測的差異
    print("利用confusion_matrix來看實際及預測的差異")
    print(confusion_matrix(y_test, rfc_pred))

    # 利用classification_report來看precision、recall、f1-score、support
    print("利用classification_report來看precision、recall、f1-score、support")
    print(classification_report(y_test, rfc_pred))

    return rfc


def actually_testData():
    idlist_text = ['*周傑倫*Jay Chou慢歌精選30首合集', 'I LOVE THIS MAN SOOOOOO MUCH!!!!!!!', '第五首是《暗號》~~~~~~~'
        , '蔣萬安', '新北市三重區中興北街42巷18、20號', 'install110@gmail.com'
        , '02-234-5586','(07)458142#7879', '03 223 7071', '35221879', '884726', '0955497502', '0955497505', 'C157873474']

    buffer = []

    for data in idlist_text:
        buffer.append(generateTrainArray(data))

    return buffer


if __name__ == '__main__':
    testData = actually_testData()
    df = pd.DataFrame(testData)
    X_test = df.drop(13, axis=1)
    print(X_test)
    model = start()
    ans = model.predict(X_test)
    print(ans)

