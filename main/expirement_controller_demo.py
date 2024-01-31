import cv2
import mediapipe as mp
import math

def hand_tracking_with_edge_highlighting_and_palm_dot():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Initialize MediaPipe Drawing
    mp_drawing = mp.solutions.drawing_utils

    # Initialize OpenCV Video Capture
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = hands.process(rgb_frame)

        # Draw hand landmarks, edges, and dot on the center of the palm
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks and edges
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract hand edges
                hand_edges = []
                for connection in mp_hands.HAND_CONNECTIONS:
                    edge_points = [hand_landmarks.landmark[connection[0]], hand_landmarks.landmark[connection[1]]]
                    hand_edges.append(edge_points)

                # Highlight hand edges
                for edge in hand_edges:
                    x1, y1 = int(edge[0].x * frame.shape[1]), int(edge[0].y * frame.shape[0])
                    x2, y2 = int(edge[1].x * frame.shape[1]), int(edge[1].y * frame.shape[0])
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Calculate the distance between middle finger tip and the wrist (base) of the hand
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                distance = math.sqrt((middle_finger_tip.x - wrist.x)**2 + (middle_finger_tip.y - wrist.y)**2)

                # Draw a dot on the center of the palm
                palm_x = int(sum([landmark.x for landmark in hand_landmarks.landmark]) / len(hand_landmarks.landmark) * frame.shape[1])
                palm_y = int(sum([landmark.y for landmark in hand_landmarks.landmark]) / len(hand_landmarks.landmark) * frame.shape[0])
                cv2.circle(frame, (palm_x, palm_y), 5, (0, 0, 255), -1)

                # Check if the hand is in a fist position
                is_fist = distance < 0.05  # Adjust this threshold as needed

                # Print "FIRE" if a fist is detected
                if is_fist:
                    cv2.putText(frame, 'FIRE', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Display the result
        cv2.imshow('Hand Tracking with Edge Highlighting and Palm Dot', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    hand_tracking_with_edge_highlighting_and_palm_dot()
