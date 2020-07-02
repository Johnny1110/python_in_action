import numpy as np
import pandas as pd
import psycopg2
import openpyxl

conn = psycopg2.connect(database="data", user="trinity", password="trinity", host="192.168.17.112", port="5432")
cursor = conn.cursor()
postgreSQL_select_Query = "select * from tp.customer a,tp.orders b where a.c_cid = b.o_cid"
cursor.execute(postgreSQL_select_Query)

results = cursor.fetchall()

for row in results:
    print("c_cid = ", row[0])
    print("c_name = ", row[1])
    print("c_sex = ", row[2])
    print("c_email = ", row[3])
    print("c_cdate = ", row[4])
    print("c_nid= ", row[5])
    print("o_oid = ", row[6])
    print("o_cid = ", row[7])
    print("o_date = ", row[8])
    print("o_status = ", row[9])
    print("o_sid = ", row[10], "\n")

df = pd.DataFrame(results)
df.to_excel('customerOrder.xlsx', sheet_name='my_sheet')



