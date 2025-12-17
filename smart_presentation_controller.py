import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Variables
pointer_mode = False
last_action_time = 0
status_text = ""
pinch_start = None

screen_w, screen_h = pyautogui.size()

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(hand_landmarks.landmark):
                lmList.append([id, int(lm.x * w), int(lm.y * h)])
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if lmList:
                # Get key points
                ix, iy = lmList[8][1], lmList[8][2]   # Index tip
                mx, my = lmList[12][1], lmList[12][2] # Middle tip
                tx, ty = lmList[4][1], lmList[4][2]   # Thumb tip

                # Check which fingers are up
                index_up = lmList[8][2] < lmList[6][2]
                middle_up = lmList[12][2] < lmList[10][2]

                # Gesture: Pinch for pointer toggle
                if abs(ix - tx) < 40 and abs(iy - ty) < 40:
                    if pinch_start is None:
                        pinch_start = time.time()
                    elif time.time() - pinch_start > 0.5 and time.time() - last_action_time > 2:
                        pointer_mode = not pointer_mode
                        status_text = f"🖱️ Pointer Mode {'ON' if pointer_mode else 'OFF'}"
                        print(status_text)
                        last_action_time = time.time()
                else:
                    pinch_start = None

                # Gesture: Next / Previous slides
                if index_up and middle_up and time.time() - last_action_time > 1:
                    pyautogui.press('right')
                    status_text = "➡️ Next Slide (Two Fingers)"
                    print(status_text)
                    last_action_time = time.time()

                elif index_up and not middle_up and time.time() - last_action_time > 1:
                    pyautogui.press('left')
                    status_text = "⬅️ Previous Slide (One Finger)"
                    print(status_text)
                    last_action_time = time.time()

                # Pointer mode movement
                if pointer_mode and index_up:
                    screen_x = int(ix * screen_w / w)
                    screen_y = int(iy * screen_h / h)
                    pyautogui.moveTo(screen_x, screen_y)

    # Show status text
    if status_text:
        cv2.putText(frame, status_text, (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Smart Presentation Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
