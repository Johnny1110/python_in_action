import joblib
import numpy as np
from sklearn import svm
import joblib


map = []


def getVector(text):
    global map
    text = text.lower()
    big_array = np.array([0.0] * len(map))
    for i in range(len(text)):
        if(i>=len(map)):
            print(text, '---->', big_array)
            return big_array
        if (map[i].get(text[i]) is None):
            big_array[i] = -100
        else:
            big_array[i] = map[i].get(text[i])

    print(text,'---->',big_array)
    return big_array



def getMap(text):
    global map
    text = text.lower()
    for i in range(len(text)):
        if(len(map)<(i+1)):
            map.append({})
        temp = map[i]
        if(temp.get(text[i])is None):
            temp[text[i]] = len(temp)*0.1
            map[i] = temp
    # print(map)


def process():
    global map
    X_train = []
    idlist_text = ['A148034958', 'B138574213', 'C114553893', 'C157873474', 'G153441612', 'G114498800', 'I167202674', 'I140247464']
    idlist_train = []
    fp = open("C:/Users/norma/OneDrive/桌面/idlist.txt", "r",encoding="utf-8")
    line = fp.readline()
    while line:
        idlist_train.append(line.split(',')[1].strip())
        line = fp.readline()
    fp.close()

    #
    # for id in idlist_train:
    #     getMap(id)
    #
    # #寫入mapping map
    # fp = open("rocid_100000.map.txt", "w", encoding="utf-8")
    # fp.write(str(map))
    # fp.close()

    #讀取mapping map
    fp = open("rocid_100000.map.txt", "r", encoding="utf-8")
    line = fp.readline()
    fp.close()
    map = eval(line)

    print(map)



    for id in idlist_train:
        X_train.append(getVector(id))
    X_train = np.array(X_train)
    #
    # print('---'*60)
    #

    # #創建訓練模型物件
    # clf = svm.OneClassSVM(nu=0.05, kernel='rbf', gamma=0.01)
    # # 訓練數據
    # clf.fit(X_train)
    # joblib.dump(clf, 'rocid_100000_model.pkl')

    #讀取model
    clf = joblib.load('rocid_100000_model.pkl')


    X_test = []
    # idlist_text = ['A148034958', 'B138574213', 'C114553893', 'C157873474', 'G153441612', 'G114498800', 'I167202674','I140247464']
    idlist_text = ['*周傑倫*Jay Chou慢歌精選30首合集', 'I LOVE THIS MAN SOOOOOO MUCH!!!!!!!', '第五首是《暗號》~~~~~~~'
        ,'蔣萬安','新北市三重區中興北街42巷18、20號','install110@gmail.com'
        ,'02-234-5586','0955497502','0955497505','C157873474']
    for id in idlist_text:
        X_test.append(getVector(id))

    X_test = np.array(X_test)
    print('X_test',X_test)

    # # 預測訓練資料
    y_pred_train = clf.predict(X_train)

    # 預測測試資料
    y_pred_test = clf.predict(X_test)

    # 輸出錯誤數量
    n_error_train = y_pred_train[y_pred_train == -1].size
    n_error_test = y_pred_test[y_pred_test == -1].size
    print('訓練資料的錯誤量', n_error_train, '正確率{}%'.format((len(X_train) - n_error_train) * 100 / len(X_train)))
    print('測試資料的錯誤量', n_error_test, '正確率{}%'.format((len(X_test) - n_error_test) * 100 / len(X_test)))
    print('程式執行完畢')




if __name__ == '__main__':
    process()
