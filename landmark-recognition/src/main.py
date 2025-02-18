import cv2
import numpy as np
import mss
import time
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

model = load_model("landmark-recognition/devotional_landmarks_v1.keras")

class_labels = [
    "Adiyogi Shiva Statue",
    "Great Buddha Statue",
    "Hazratbal Shrine",
    "Velankanni Church",
]

sct = mss.mss()
monitor = {"top": 100, "left": 100, "width": 800, "height": 600}

FRAME_RATE = 5
cv2.namedWindow("Landmark Recognition", cv2.WINDOW_NORMAL)

try:
    while True:
        start_time = time.time()

        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

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

        elapsed_time = time.time() - start_time
        time.sleep(max(1.0 / FRAME_RATE - elapsed_time, 0))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("\n[INFO] Program interrupted by user.")

finally:
    print("\n[INFO] Cleaning up resources...")
    cv2.destroyAllWindows()
