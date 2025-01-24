import cv2
import os
import time

camera = cv2.VideoCapture(0)
name = input("Enter the person's name: ").strip()
os.makedirs(f"dataset/{name}", exist_ok=True)

count = 0
start_time = time.time()

while count < 50:
    ret, frame = camera.read()
    if not ret:
        break
    if time.time() - start_time >= 1:
        cv2.imwrite(f"dataset/{name}/{name}_{count+1}.jpg", frame)
        count += 1
        start_time = time.time()
    cv2.imshow("Capture Photos", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
