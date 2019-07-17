import cv2
import os
import pymysql
import base64
import numpy as np


sample_set = ["Look Straight ", "Look slightly up ",
              "Look slightly upper left ", "Look slightly left ",
              "Look slightly lower left ", "Look slightly down ",
              "Look slightly lower right ", "Look slightly right ",
              "Look slightly upper right ", "Smile "]

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

conn = pymysql.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="Project"
)

mycursor = conn.cursor()


def save_image(id, image, query):
    as_array = np.array(image)
    shape = as_array.shape
    height = shape[0]
    width = shape[1]
    as_bytes = as_array.tobytes()
    encoded_bytes = base64.b16encode(as_bytes)
    Details = (id, height, width, encoded_bytes)
    mycursor.execute(query, Details)
    conn.commit()


sql1 = "INSERT INTO Students (id, fname, lname) VALUES (%s,%s,%s)"

face_id = int(input("\nEnter user's id: \n"))
fname = input('\nEnter First name : \n')
lname = input('\nEnter Last name: \n')

details = (face_id, fname, lname)
mycursor.execute(sql1, details)
conn.commit()

sql2 = "INSERT into Images (id, height, width, image) VALUES(%s,%s,%s,%s)"

font = cv2.FONT_HERSHEY_SIMPLEX

cam = cv2.VideoCapture(0)
cam.set(3, 1200)
cam.set(4, 800)

count = 0
count2=-1

while(True):
    ret, img = cam.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        text = sample_set[count]+"and press 's'"
        cv2.putText(img, text, (10, 20), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        img1 = gray[y-50:y+h+50,x-50:x+w+50]
    cv2.imshow('image', img)

    if count2==3:
        count2=-1
        count+=1
    if count2>=0:
        count2 += 1
        save_image(face_id, img1, sql2)
        continue

    if count >= len(sample_set):
        break

    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif k == 115:
        count2=0
        save_image(face_id, img1, sql2)


cam.release()
cv2.destroyAllWindows()