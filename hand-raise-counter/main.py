import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

count = 0
hand_raised_threshold = 0.5
hand_state = "HAND_DOWN"
last_hand_raised_time = 0
debounce_time = 1

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        current_time = time.time()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
                middle_finger_y = hand_landmarks.landmark[
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP
                ].y
                distance = wrist_y - middle_finger_y

                if distance >= hand_raised_threshold:
                    if (
                        hand_state == "HAND_DOWN"
                        and (current_time - last_hand_raised_time) > debounce_time
                    ):
                        hand_state = "HAND_UP"
                        count += 1
                        last_hand_raised_time = current_time
                        print(f"Count: {count}")
                else:
                    hand_state = "HAND_DOWN"

                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

        cv2.putText(
            frame,
            f"Count: {count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
        )
        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    cap.release()
    cv2.destroyAllWindows()
