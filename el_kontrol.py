import cv2
import mediapipe as mp
import pyautogui
import time

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x = None
slide_cooldown = 0

while True:
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            mouse_x = screen_w * hand_landmarks.landmark[8].x
            mouse_y = screen_h * hand_landmarks.landmark[8].y
            pyautogui.moveTo(mouse_x, mouse_y)

            thumb_x = hand_landmarks.landmark[4].x
            thumb_y = hand_landmarks.landmark[4].y
            index_x = hand_landmarks.landmark[8].x
            index_y = hand_landmarks.landmark[8].y

            distance = ((thumb_x-index_x)**2 + (thumb_y-index_y)**2)**0.5

            if distance < 0.03:
                pyautogui.click()
                time.sleep(0.3)

            if prev_x is not None:
                diff = x - prev_x

                if time.time() > slide_cooldown:
                    if diff > 60:
                        pyautogui.press("right")
                        slide_cooldown = time.time() + 1
                    elif diff < -60:""
                        pyautogui.press("left")
                        slide_cooldown = time.time() + 1

            prev_x = x

    cv2.imshow("El Kontrol", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
