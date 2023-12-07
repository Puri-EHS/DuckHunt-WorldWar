# Taken over by Alex, bitch
import cv2
import numpy as np
from scipy import stats

class Tracker:
    def __init__(self):
        # Set the camera index (0 for the default camera)
        self.camera_index = 0

        # Provide the paths to the icon images
        self.icon1_path = 'assets/New_fedu.png'
        self.icon2_path = 'assets/New_fedu.png'
        # Load the icon images
        self.icon1 = cv2.imread(self.icon1_path, cv2.IMREAD_UNCHANGED)
        self.icon1_gray = cv2.cvtColor(self.icon1, cv2.COLOR_BGR2GRAY)
        # Create a SIFT detector
        self.sift = cv2.SIFT_create()

        # Detect keypoints and compute descriptors for the icons
        self.kp_icon1, self.des_icon1 = self.sift.detectAndCompute(self.icon1_gray, None)
        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)
        # Pre-stabilized coords
        self.avg_x = 0
        self.avg_y = 0

        # Points used for stabilizing motion: [ACCESS THESE POINTS FOR COORDS]
        self.stable_avg_x = 0
        self.stable_avg_y = 0

        self.num_fire = 0


    def track_icons(self, camera_index=0, icon1_path='main/New_fedu.png', icon2_path='main/New_fedu.png'):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        # Resize frame to improve speed, but reduce accuracy
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
        # Convert the frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect keypoints and compute descriptors for the frame
        kp_frame, des_frame = self.sift.detectAndCompute(frame_gray, None)

        # Create a BFMatcher (Brute-Force Matcher) object
        bf = cv2.BFMatcher()

        # Match descriptors for icon 1
        matches_icon1 = bf.knnMatch(self.des_icon1, des_frame, k=2)

        # Apply ratio test to filter good matches for icon 1
        good_matches_icon1 = []
        for m, n in matches_icon1:
            if m.distance < 0.70 * n.distance:
                good_matches_icon1.append(m)

        

    # Outlier Rejection System (Helps clean up data from random points)
        x_values = [kp_frame[m.trainIdx].pt[0] for m in good_matches_icon1]
        y_values = [kp_frame[m.trainIdx].pt[1] for m in good_matches_icon1]
        z_scores_x = np.abs(stats.zscore(x_values))
        z_scores_y = np.abs(stats.zscore(y_values))

        # Combine Z-scores for x and y dimensions2
        z_scores_combined = np.sqrt(z_scores_x**2 + z_scores_y**2)

        # Identify outliers based on the threshold
        outliers = np.where(z_scores_combined > 2)[0]

        # Remove outliers from the original list
        filtered_points = [point for i, point in enumerate(good_matches_icon1) if i not in outliers]
        good_matches_icon1 = filtered_points
        


    
        if len(good_matches_icon1) >= 2:
            self.avg_x = 1800-(int(np.mean([kp_frame[m.trainIdx].pt[0] for m in good_matches_icon1]))*4)
            self.avg_y = (int(np.mean([kp_frame[m.trainIdx].pt[1] for m in good_matches_icon1])) * 4) - 1000

            # Noise elimination sysetem (Smoothing of stuttery motion)
            if self.avg_x - self.stable_avg_x > 10 or self.avg_x - self.stable_avg_x < -10:
                self.stable_avg_x = self.avg_x
            if self.avg_y - self.stable_avg_y > 10 or self.avg_y - self.stable_avg_y < -10:
                self.stable_avg_y = self.avg_y


            print(self.stable_avg_y, self.stable_avg_y)
            self.num_fire = 0

        else:
            print("FIRE")
            self.num_fire += 1

