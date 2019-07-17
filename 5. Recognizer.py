import cv2
import pymysql
import random
import datetime

text = {
    "greeting":["Hello {}",
                "Good Morning, {},"]
}

conn = pymysql.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="Project"
)

mycursor = conn.cursor()

def create_column():
    today = datetime.date.today()
    today = str(today).split('-')
    sql = "ALTER TABLE Attendance ADD Date_{} VARCHAR(255) DEFAULT 'ABSENT'".format(today[2])
    mycursor.execute(sql)


def check_present(id):
    today = datetime.date.today()
    today = str(today).split('-')
    sql = "SELECT Date_{} from Attendance where id = '{}'".format(today[2],id)
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    if myresult[0] == "ABSENT":
        return 0
    else:
        return 1


def mark_present(id):
    today = datetime.date.today()
    today = str(today).split('-')
    sql = "UPDATE Attendance SET Date_{} = 'PRESENT' WHERE id='{}'".format(today[2], id)
    print("Updated")
    mycursor.execute(sql)
    conn.commit()


def greet_Student(id):
    sql1 = "SELECT fname from Students WHERE id={}".format(id)
    mycursor.execute(sql1)
    myresult = mycursor.fetchone()
    if myresult:
        greeting = text['greeting'][random.randrange(0, len(text['greeting']))]
        print(greeting.format(myresult[0]))
        return myresult[0]
    else:
        return "Does Not Exist"


create_column()
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


font = cv2.FONT_HERSHEY_SIMPLEX
id = 0

cam = cv2.VideoCapture(0)
cam.set(3, 1200)
cam.set(4, 800)

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5,)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        if (confidence < 100):
            if check_present(id)==0:
                mark_present(id)
                greet_Student(id)
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()