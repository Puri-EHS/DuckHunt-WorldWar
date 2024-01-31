import cv2
import mediapipe as mp

def hand_tracking_with_edge_and_dot_highlighting():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Initialize MediaPipe Drawing
    mp_drawing = mp.solutions.drawing_utils

    # Initialize OpenCV Video Capture
    cap = cv2.VideoCapture(0)

    # Offset for the dot above the detected hand
    dot_offset = (0, -100)  # Adjust the values based on your preference

    while cap.isOpened():
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = hands.process(rgb_frame)

        # Draw hand landmarks, edges, and dot
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
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

                # Calculate the position of the dot above the middle finger's PIP joint (closer to the wrist)
                dot_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x * frame.shape[1]) + dot_offset[0]
                dot_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * frame.shape[0]) + dot_offset[1]

                # Draw the dot
                cv2.circle(frame, (dot_x, dot_y), 5, (255, 0, 0), -1)

        # Display the result
        cv2.imshow('Hand Tracking with Edge and Dot Highlighting', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    hand_tracking_with_edge_and_dot_highlighting()
