import numpy as np
import pandas as pd
import psycopg2
import openpyxl

df1 = pd.DataFrame({'City': ['New York', 'Chicago', 'Tokyo', 'Paris', 'New Delhi'],
                    'Column1': [55, 55, 73, 85, 56], 'Column2': [5, 5, 7, 8, 10]})
df2 = pd.DataFrame({'City': ['New York', 'Chicago', 'Tokyo', 'Paris', 'New Delhi'],
                    'Column1': [55, 55, 73, 85, 56], 'Column2': [5, 6, 7, 8, 9]})

test = pd.concat([df1,df2])
#print(test.info)

merged = df1.merge(df2, indicator=True, how='outer')
final = merged.loc[merged['_merge'] == 'left_only']


print(final.info)