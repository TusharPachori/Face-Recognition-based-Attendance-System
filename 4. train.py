import pymysql
import base64
import cv2
import numpy as np
import os


conn = pymysql.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="Project"
)

mycursor = conn.cursor()

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

sql1 = "SELECT id from Images"

mycursor.execute(sql1)
myresult = mycursor.fetchall()
ids = set()
for i in myresult:
    ids.add(i[0])

id_list = []
face_sample_list = []

for i in ids:
    sql2 = "Select * from Images WHERE id={}".format(i)
    mycursor.execute(sql2)
    myresult = mycursor.fetchall()
    for result in myresult:
        id = result[0]
        height = result[1]
        width = result[2]
        as_bytes = base64.b16decode(result[3])
        array_shape = (height, width)
        img = np.frombuffer(as_bytes, dtype = 'uint8').reshape(array_shape)
        faces = detector.detectMultiScale(img)
        for (x,y,w,h) in faces:
            id_list.append(id)
            face_sample_list.append(img[y:y+h,x:x+w])

recognizer.train(face_sample_list, np.array(id_list))
recognizer.write('trainer.yml')
