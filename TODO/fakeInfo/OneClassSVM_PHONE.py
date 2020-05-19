import csv

import jieba
import pandas as pd

from TODO.fakeInfo.utils import getTData
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

dict_map = {}

def buildDict(input_map, train_source, split):
    global dict_map

    if input_map:
        dict_map = input_map
        return

    if split.__eq__("jieba"):
        mapVal = 1
        for row in train_source:
            data = row[0]
            seg_list = jieba.cut(data, cut_all=False)
            for seg in seg_list:
                try:
                    dict_map[seg]
                except Exception:
                    dict_map[seg] = mapVal
                    mapVal += 1

    if split.__eq__("char"):
        mapVal = 1
        for row in train_source:
            data = row[0]
            for char in data:
                try:
                    dict_map[char]
                except Exception:
                    dict_map[char] = mapVal
                    mapVal += 1


def mapedTrainSource(train_source):
    result = []
    for row in train_source:
        text = row[0]
        label = row[1]

        word_length = len(text)
        buffer_max = 20
        buffer = [0 for i in range(buffer_max)]

        for i in range(word_length):
            if i > 17:
                break

            # 先使用字典映射 phoneNum
            try:
                mapped_word = dict_map[text[i]]
                buffer[i] = mapped_word
            except:
                buffer[i] = 0

        buffer[18] = word_length  # 第 18 欄加入號碼長度
        buffer[19] = int(label)  # 第 19 欄加入號碼長度

        result.append(buffer)
    return result

def mapedActSource(act_source):
    result = []
    for text in act_source:

        word_length = len(text)
        buffer_max = 19
        buffer = [0 for i in range(buffer_max)]

        for i in range(word_length):
            if i > 17:
                break

            # 先使用字典映射 phoneNum
            try:
                mapped_word = dict_map[text[i]]
                buffer[i] = mapped_word
            except:
                buffer[i] = 0
        buffer[18] = word_length  # 第 18 欄加入號碼長度
        result.append(buffer)

    return result

def start(train_source, input_map=None, split="jieba"):
    buildDict(input_map, train_source, split)  # 先切 MAP
    maped_Train_data = mapedTrainSource(train_source)
    df = pd.DataFrame(maped_Train_data)

    # 將資料分成訓練組及測試組
    # 因為 index(13) 是之後要預測的變數，所以X軸不用
    X = df.drop(19, axis=1)
    print(X)
    y = df[19]
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




if __name__ == '__main__':
    sourceTrainData = getTData("data.csv")
    model = start(sourceTrainData, split="char")

    idlist_text = ['*周傑倫*Jay Chou慢歌精選30首合集', 'I LOVE THIS MAN SOOOOOO MUCH!!!!!!!', '第五首是《暗號》~~~~~~~'
        , '蔣萬安', '813 新北市三重區中興北街42巷18、20號','114 台北市內湖區民權東路六段23號', 'install110@gmail.com'
        , '02-234-5586', '(07)458142#7879', '03 223 7071', '35221879', '884726', '0955497502', '0955497505',
                   'C157873474']

    act_list = mapedActSource(idlist_text)
    df = pd.DataFrame(act_list)
    result = model.predict(df)
    print(result)

