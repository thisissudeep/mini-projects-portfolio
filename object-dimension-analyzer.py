from ultralytics import YOLO
import cv2


model = YOLO("yolov8s.pt")


KNOWN_WIDTH = 25.0
FOCAL_LENGTH = 500


def calculate_real_dimensions(
    known_width, focal_length, perceived_width, perceived_height
):
    real_width = (known_width * focal_length) / perceived_width
    real_height = (perceived_height / perceived_width) * real_width
    return real_width, real_height


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        names = result.names

        for box, confidence, class_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = box
            perceived_width = x2 - x1
            perceived_height = y2 - y1

            real_width, real_height = calculate_real_dimensions(
                KNOWN_WIDTH, FOCAL_LENGTH, perceived_width, perceived_height
            )

            object_name = names[class_id]
            label = f"{object_name} | W: {real_width:.1f}cm, H: {real_height:.1f}cm"

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            text_position = (int(x1), int(y1) - 15)
            cv2.putText(
                frame,
                label,
                text_position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )

    cv2.imshow("Real-Time Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
