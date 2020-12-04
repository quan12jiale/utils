import sqlite3

old_db = r"C:\Users\quanjl\Desktop\GBCQTransData.db"
new_db = r"E:\GFCFile\GBCQTransData.db"

tblCmp = "SELECT * FROM EdoReport order by EDOID"

conn1 = sqlite3.connect(old_db)
conn2 = sqlite3.connect(new_db)

cursor1 = conn1.cursor()
result1 = cursor1.execute(tblCmp)
res1 = result1.fetchall()

cursor2 = conn2.cursor()
result2 = cursor2.execute(tblCmp)
res2 = result2.fetchall()

conn1.close()
conn2.close()

res1 = set(res1)
res2 = set(res2)
result = res1.symmetric_difference(res2)

# 原组件化 - 现组件化的差集
result1 = res1.difference(res2)
# 现组件化 - 原组件化的差集
result2 = res2.difference(res1)