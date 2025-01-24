import cv2
from ultralytics import YOLO
from collections import defaultdict
from datetime import datetime
import json
import time

model = YOLO("yolov5n.pt")

# video_path = "D:/ss2.mp4"
cap = cv2.VideoCapture(0)
person_id = 0
person_tracker = {}
interaction_data = defaultdict(
    lambda: {
        "initial_objects": set(),
        "interactions": defaultdict(int),
        "contacted_objects": set(),
        "first_detected": None,
        "last_detected": None,
        "total_time": 0,
        "person_interactions": set(),
        "objects_at_end": set(),
    }
)
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
last_update_time = time.time()

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
                person_tracker[pid]["last_detected"] = datetime.now()
                interaction_data[pid]["last_detected"] = datetime.now()
                tracked = True
                break

        if not tracked:
            person_id += 1
            person_tracker[person_id] = {
                "bbox": (x1, y1, x2, y2),
                "frames": 1,
                "first_detected": datetime.now(),
                "last_detected": datetime.now(),
                "contacted_objects": set(),
                "person_interactions": set(),
            }
            interaction_data[person_id]["first_detected"] = datetime.now()
            interaction_data[person_id]["last_detected"] = datetime.now()

    for pid, data in person_tracker.items():
        px1, py1, px2, py2 = data["bbox"]

        for obj_bbox, obj_label in frame_objects:
            ox1, oy1, ox2, oy2 = map(int, obj_bbox)
            if (px1 < ox2 and px2 > ox1) and (py1 < oy2 and py2 > oy1):
                if obj_label not in data["contacted_objects"]:
                    interaction_data[pid]["interactions"][obj_label] += 1
                    interaction_data[pid]["contacted_objects"].add(obj_label)

    for pid, data in person_tracker.items():
        for other_pid, other_data in person_tracker.items():
            if pid != other_pid:
                px1, py1, px2, py2 = data["bbox"]
                ox1, oy1, ox2, oy2 = other_data["bbox"]
                if (px1 < ox2 and px2 > ox1) and (py1 < oy2 and py2 > oy1):
                    interaction_data[pid]["person_interactions"].add(
                        f"person_{other_pid}"
                    )

    for pid, data in person_tracker.items():
        if (datetime.now() - data["first_detected"]).total_seconds() <= 5:
            for obj_bbox, obj_label in frame_objects:
                ox1, oy1, ox2, oy2 = map(int, obj_bbox)
                if (px1 < ox2 and px2 > ox1) and (py1 < oy2 and py2 > oy1):
                    interaction_data[pid]["initial_objects"].add(obj_label)

    for pid, data in person_tracker.items():
        if (datetime.now() - data["first_detected"]).total_seconds() > 5:
            for obj_bbox, obj_label in frame_objects:
                ox1, oy1, ox2, oy2 = map(int, obj_bbox)
                if (px1 < ox2 and px2 > ox1) and (py1 < oy2 and py2 > oy1):
                    interaction_data[pid]["objects_at_end"].add(obj_label)

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

    if time.time() - last_update_time >= 5:
        interaction_summary = {}
        for pid, data in interaction_data.items():
            total_time = (
                (data["last_detected"] - data["first_detected"]).total_seconds()
                if data["first_detected"] and data["last_detected"]
                else 0
            )
            interaction_summary[f"person_{pid}"] = {
                "first_detected": data["first_detected"].isoformat(),
                "last_detected": data["last_detected"].isoformat(),
                "total_time": total_time,
                "initial_objects": list(data["initial_objects"]),
                "interactions": {k: v for k, v in data["interactions"].items()},
                "person_interactions": list(data["person_interactions"]),
                "objects_at_end": list(data["objects_at_end"]),
            }

        with open("interaction_data.json", "w") as json_file:
            json.dump(interaction_summary, json_file, indent=4)

        last_update_time = time.time()

cap.release()
cv2.destroyAllWindows()

print("Interaction data has been stored in 'interaction_data.json'.")
