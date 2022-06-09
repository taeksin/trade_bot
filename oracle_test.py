import cx_Oracle
import os 

LOCATION = r"D:\개발툴\oracle_SQL\instantclient_21_3" #로컬.
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"] #환경변수 등록
OracleConnect = cx_Oracle.connect("ID", "PASS", "IP:PORT/서비스이름")
OracleCursor = OracleConnect.cursor()


oracleSql = f"""
    쿼리
"""
#print(oracleSql)
OracleCursor.execute(oracleSql)

for i in OracleCursor:
    print(i)