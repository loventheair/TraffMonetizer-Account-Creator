import mysql.connector

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
try:
    mycursor = mydb.cursor()
except Exception as db_error:
    print(f"MySQL Connection Error: {db_error}")


sql = "SELECT * FROM servers"

mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
  print(f"{x}")
