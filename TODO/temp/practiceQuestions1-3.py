import numpy as np
import pandas as pd
import zipfile
from os import listdir
from os.path import isfile, isdir, join
from os import walk



df = pd.DataFrame(pd.read_csv('orders.txt'))
df2 = pd.DataFrame(pd.read_csv('sales.txt'))

#print(df.info)
#print(df2.info)

dfm = pd.merge(df, df2, left_on='o_sid', right_on='s_sid', how='left')

print(dfm.info)

dfm.to_csv('mergeTable.txt')

#with zipfile.ZipFile('mergeTable.zip', 'w') as zf:
    #zf.write('mergeTable.txt')



mypath = "C:/Users/LenovoYoga/PycharmProjects/MyProject"

files = listdir(mypath)


for root, dirs, files in walk(mypath):
  print("路徑：", root)
  print("   目錄：", dirs)
  print("   檔案：", files)






