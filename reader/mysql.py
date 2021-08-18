import pymysql

# Simple routine to run a query on a database and print the results: 

myConnection = pymysql.connect(
  host="127.0.0.1",
  port=3306,
  user="root",
  password="password",
  autocommit=True
)

cur = myConnection.cursor()
#cur.execute("INSERT INTO text.Files (full_name) VALUES ('manual_ps5');")
cur.fetchall()
myConnection.close()

