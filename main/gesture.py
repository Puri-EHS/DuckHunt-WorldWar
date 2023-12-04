import cv2
import mediapipe as mp

def get_points(queue):
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
        
        if queue is not None:
            queue.put((tip, nuckle))
        
#        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                


if __name__ == "__main__":
    get_points(None)
