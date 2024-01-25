import cv2
import numpy as np
from scipy import stats

class ControllerTrackDemo:


    def  __init__(self):
        # Set the camera index (0 for the default camera)
        camera_index = 0

        # Provide the paths to the icon images
        icon1_path = '/Users/soarece/Downloads/New_fedu.png'
        icon2_path = '/Users/soarece/Downloads/New_fedu.png'

        # Load the icon images
        icon1 = cv2.imread(icon1_path, cv2.IMREAD_UNCHANGED)
        icon1_gray = cv2.cvtColor(icon1, cv2.COLOR_BGR2GRAY)

        #icon2 = cv2.imread(icon2_path, cv2.IMREAD_UNCHANGED)
        #icon2_gray = cv2.cvtColor(icon2, cv2.COLOR_BGR2GRAY)

        # Create a SIFT detector
        sift = cv2.SIFT_create()

        # Detect keypoints and compute descriptors for the icons
        kp_icon1, des_icon1 = sift.detectAndCompute(icon1_gray, None)
        #kp_icon2, des_icon2 = sift.detectAndCompute(icon2_gray, None)

        # Create a VideoCapture object
        cap = cv2.VideoCapture(camera_index)
    

        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            if not ret:
                print("Error reading frame")
                break
            
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
            # Convert the frame to grayscale
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect keypoints and compute descriptors for the frame
            kp_frame, des_frame = sift.detectAndCompute(frame_gray, None)

            # Create a BFMatcher (Brute-Force Matcher) object
            bf = cv2.BFMatcher()

            # Match descriptors for icon 1
            matches_icon1 = bf.knnMatch(des_icon1, des_frame, k=2)

            # Apply ratio test to filter good matches for icon 1
            good_matches_icon1 = []

            if len(matches_icon1) >0:
                if len(matches_icon1[0]) > 1:
                    for m, n in matches_icon1:
                        if m.distance < 0.70 * n.distance:
                            good_matches_icon1.append(m)

            

        # Outlier Rejection System (Helps clean up data from random points)
            x_values = [kp_frame[m.trainIdx].pt[0] for m in good_matches_icon1]
            y_values = [kp_frame[m.trainIdx].pt[1] for m in good_matches_icon1]

            z_scores_x = np.abs(stats.zscore(x_values))
            z_scores_y = np.abs(stats.zscore(y_values))

            # Combine Z-scores for x and y dimensions
            z_scores_combined = np.sqrt(z_scores_x**2 + z_scores_y**2)

            # Identify outliers based on the threshold
            outliers = np.where(z_scores_combined > 2)[0]

            # Remove outliers from the original list
            filtered_points = [point for i, point in enumerate(good_matches_icon1) if i not in outliers]
            good_matches_icon1 = filtered_points
            not_enough_points = []


            # Match descriptors for icon 2
            #matches_icon2 = bf.knnMatch(des_icon2, des_frame, k=2)

            # Apply ratio test to filter good matches for icon 2
            #good_matches_icon2 = []
            #for m, n in matches_icon2:
                #if m.distance < 0.75 * n.distance:
                    #good_matches_icon2.append(m)

            # Draw matches on the frame for icon 1
            if len(good_matches_icon1) > 7:
                img_matches_icon1 = cv2.drawMatches(icon1, kp_icon1, frame, kp_frame, good_matches_icon1, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            else:
                img_matches_icon1 = cv2.drawMatches(icon1, kp_icon1, frame, kp_frame, not_enough_points, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            # Draw matches on the frame for icon 2
            #img_matches_icon2 = cv2.drawMatches(icon2, kp_icon2, frame, kp_frame, good_matches_icon2, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            if len(good_matches_icon1) > 7:
                avg_x = int(np.mean([kp_frame[m.trainIdx].pt[0] for m in good_matches_icon1]))
                avg_y = int(np.mean([kp_frame[m.trainIdx].pt[1] for m in good_matches_icon1]))
                print(avg_x, avg_y)
            else:
                print("FIRE")

            
            # Display the frames with the tracked icons
            cv2.imshow('Track Demo: [PRESS Q to exit]', img_matches_icon1)
            #cv2.imshow('Tracked Icon 2', img_matches_icon2)
            
            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the VideoCapture and close all windows
        cap.release()
        cv2.destroyAllWindows()


