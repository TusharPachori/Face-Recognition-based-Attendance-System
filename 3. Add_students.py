import pymysql


conn = pymysql.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="Project"
)
mycursor = conn.cursor()

# sql1 = "SELECT id from Students"
# sql2 = "INSERT INTO Attendance (id) VALUES (%s)"
#
# mycursor.execute(sql1)
# myresult = mycursor.fetchall()
# ids = set()
# for i in myresult:
#     ids.add(i[0])
#
#
# for id in ids:
#     mycursor.execute(sql2, (id,))
#
# conn.commit()

sql = "Select * from Attendance"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for i in myresult:
    print(i)