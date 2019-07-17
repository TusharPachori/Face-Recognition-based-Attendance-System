import pymysql

conn = pymysql.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="Project"
)

mycursor = conn.cursor()

mycursor.execute("CREATE TABLE Students (id INT PRIMARY KEY, fname VARCHAR(255), lname VARCHAR(255))")
mycursor.execute("CREATE TABLE Images (id INT, height INT, width INT, image LONGBLOB)")
mycursor.execute("CREATE TABLE Attendance (id INT AUTO_INCREMENT PRIMARY KEY)")

# mycursor.execute("Drop TABLE Images")
# mycursor.execute("Drop TABLE Attendance")
