import face_recognition
import os
import pickle

data = []
labels = []
for person_name in os.listdir("dataset"):
    person_path = f"dataset/{person_name}"
    for img_name in os.listdir(person_path):
        img_path = f"{person_path}/{img_name}"
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            data.append(encodings[0])
            labels.append(person_name)

with open("face_encodings.pkl", "wb") as f:
    pickle.dump({"encodings": data, "names": labels}, f)
