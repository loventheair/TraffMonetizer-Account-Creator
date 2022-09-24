import mysql.connector

mydb = mysql.connector.connect(
    host="byte.rasbyte.net",
    user="admin_omer",
    password="@But@!ib$iriy3v200311",
    database="admin_omer"
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