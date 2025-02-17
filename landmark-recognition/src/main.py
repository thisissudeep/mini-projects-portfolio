import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

model = load_model("devotional_landmarks_v1.keras")

class_labels = [
    "Adiyogi Shiva Statue",
    "Great Buddha Statue",
    "Hazratbal Shrine",
    "Velankanni Church",
]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.resize(frame, (224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_label = class_labels[predicted_class]

    cv2.putText(
        frame,
        f"Landmark: {predicted_label}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.imshow("Landmark Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
