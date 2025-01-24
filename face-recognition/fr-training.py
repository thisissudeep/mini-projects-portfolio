import cv2
import os
import numpy as np

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
recognizer = cv2.face.LBPHFaceRecognizer_create()


def train_model():
    data_dir = "Dataset"
    labels = []
    faces = []
    names = {}
    current_id = 0

    for person_name in os.listdir(data_dir):
        person_path = os.path.join(data_dir, person_name)
        if os.path.isdir(person_path):
            names[current_id] = person_name
            for img_name in os.listdir(person_path):
                img_path = os.path.join(person_path, img_name)
                img = cv2.imread(img_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces_detected = face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5
                )
                for x, y, w, h in faces_detected:
                    faces.append(gray[y : y + h, x : x + w])
                    labels.append(current_id)
            current_id += 1

    recognizer.train(faces, np.array(labels))
    recognizer.save("trained_model.yml")
    np.save("names.npy", names)


train_model()
