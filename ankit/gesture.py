import cv2
import mediapipe as mp
import math

def get_points(queue, tix, tiy, tiz, nucky, nuckz):
    hands = mp.solutions.hands.Hands(max_num_hands=1)
    cap = cv2.VideoCapture(0)

    print("gesture loop started")

    tip = None
    nuckle = None

    while True:

        ret, frame = cap.read()
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # get index finger landmark
        if result.multi_hand_landmarks:
            for hand_landmark in result.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmark, mp.solutions.hands.HAND_CONNECTIONS)
                for id, landmark in enumerate(hand_landmark.landmark):
                    if id == 8:
                        tip = landmark
                    if id == 5:
                        nuckle = landmark
        
        if queue is not None and tip is not None and nuckle is not None:
            queue.put((tip, nuckle))
            tix.value = tip.x
            tiy.value = tip.y
            tiz.value = tip.z
            nuckz.value = nuckle.z
            nucky.value = nuckle.y

        
        # cv2.imshow("frame", frame)
        # if tip is not None and nuckle is not None:
        #     print(math.atan((tip.y - nuckle.y)/ (tip.z - nuckle.z)) * 180 / math.pi)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                


if __name__ == "__main__":
    get_points(None)
