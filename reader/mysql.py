import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  port="3306",
  user="user",
  password="password"
)

cursor = mydb.cursor()

cursor.execute("show databases")

print(cursor.fetchall())

cursor.close()

# To initialize de container
# docker-compose up
# winpty docker exec -ti professor-virtual_db_1 mysql -u root -p