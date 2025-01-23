import cv2
import json
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
from datetime import datetime

model = YOLO("yolov8n.pt")

video_path = "videopath"
cap = cv2.VideoCapture(video_path)


person_id = 0
person_tracker = {}
interaction_data = defaultdict(
    lambda: {"interactions": defaultdict(int), "total_time": 0}
)
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, stream=True)

    frame_objects = []
    persons = []

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "person":
                persons.append((box.xyxy[0], cls))
            else:
                frame_objects.append((box.xyxy[0], label))

    for person_bbox, cls in persons:
        x1, y1, x2, y2 = map(int, person_bbox)

        tracked = False
        for pid, data in person_tracker.items():
            px1, py1, px2, py2 = data["bbox"]
            if (px1 - 50 <= x1 <= px2 + 50) and (py1 - 50 <= y1 <= py2 + 50):
                person_tracker[pid]["bbox"] = (x1, y1, x2, y2)
                person_tracker[pid]["frames"] += 1
                tracked = True
                break

        if not tracked:
            person_id += 1
            person_tracker[person_id] = {"bbox": (x1, y1, x2, y2), "frames": 1}

    for pid, data in person_tracker.items():
        px1, py1, px2, py2 = data["bbox"]

        for obj_bbox, obj_label in frame_objects:
            ox1, oy1, ox2, oy2 = map(int, obj_bbox)
            if (px1 < ox2 and px2 > ox1) and (py1 < oy2 and py2 > oy1):
                interaction_data[pid]["interactions"][obj_label] += 1
                interaction_data[pid]["total_time"] += 1 / frame_rate

    for pid, data in person_tracker.items():
        x1, y1, x2, y2 = data["bbox"]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Person {pid}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    for obj_bbox, obj_label in frame_objects:
        x1, y1, x2, y2 = map(int, obj_bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(
            frame,
            obj_label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            2,
        )

    cv2.imshow("YOLO Object and Person Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()


interaction_summary = {}
for pid, data in interaction_data.items():
    interaction_summary[pid] = {
        "total_time": round(data["total_time"], 2),
        "interactions": {k: v for k, v in data["interactions"].items()},
    }


output_json_path = (
    f"interaction_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
)
with open(output_json_path, "w") as json_file:
    json.dump(interaction_summary, json_file, indent=4)

print(f"Interaction data saved to {output_json_path}")
