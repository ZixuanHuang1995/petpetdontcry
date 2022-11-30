import sqlite3
import pandas as pd
# 讀csv檔
df = pd.read_csv('/Users/tzu/Desktop/QQ.csv')
print(df)

# 為了整理用藥資料
# df = df['name'].dropna(axis=0,how='any',inplace=False)
# df['type'] = 1
# df['name'] = df['A'].str.cat([df.B],sep=' ')
# df['function'] = df['C'].str.cat([df.D,df.E,df.F],sep=' ')
# df = df.drop(['A','B','C','D','E','F'],axis=1)
# df = df.dropna(axis=0,how='any')

# 連DB
conn = sqlite3.connect('/Users/tzu/Desktop/pet/instance/petpetdontcry.sqlite3')
# 建立資料(要注意欄位名稱要一樣，不能多不能少，除了ID)
df.to_sql('user',conn , if_exists='append' , index=False)
#透過SQL語法讀取資料庫中的資料
us_df = pd.read_sql("SELECT * FROM user ", conn)
print(us_df)