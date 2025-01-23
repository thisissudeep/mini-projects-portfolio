import torch
import cv2

model = torch.hub.load("ultralytics/yolov5", "yolov5s")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame)
    results.render()
    cv2.imshow("YOLOv5 Real-Time Object Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
