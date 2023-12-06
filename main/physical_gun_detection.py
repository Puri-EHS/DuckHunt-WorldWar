#Taken over by Alex, bitch
import cv2
import numpy as np

class Tracker:
    
    def __init__(self) -> None:
        # Set the camera index (0 for the default camera)
        self.camera_index = 0

        # Provide the paths to the icon images
        self.avg_x = 0  #current detected icon location
        self.avg_y = 0

        self.icon1 = cv2.imread('main/New_fedu.png', cv2.IMREAD_UNCHANGED) #set what icon to track
        self.icon1_gray = cv2.cvtColor(self.icon1, cv2.COLOR_BGR2GRAY)

        # Create a SIFT detector
        self.sift = cv2.SIFT_create()

        # Detect keypoints and compute descriptors for the icons
        self.kp_icon1, self.des_icon1 = self.sift.detectAndCompute(self.icon1_gray, None)

        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)
        self.firing = False

    def track_icons(self, camera_index=0, icon1_path='main/New_fedu.png', icon2_path='main/New_fedu.png'):
        # Load the icon images
        # Read a frame from the camera
        ret, frame = self.cap.read()

        frame = cv2.resize(frame, None, fx=0.75, fy=0.75)
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
            if m.distance < 0.75 * n.distance:
                good_matches_icon1.append(m)

        #img_matches_icon2 = cv2.drawMatches(icon2, kp_icon2, frame, kp_frame, good_matches_icon2, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        
        if len(good_matches_icon1) > 2: #If more than 2 points, assume icon exists and find average to estimate icon center
            
            #reverse for camera with 720 by 1080 resolution, scaled to 540 by 810
            #Game width 758, half being 379
            self.avg_x = 540 - int(np.mean([kp_frame[m.trainIdx].pt[0] for m in good_matches_icon1])) + 379
            self.avg_y = int(np.mean([kp_frame[m.trainIdx].pt[1] for m in good_matches_icon1]))
            
            print(self.avg_x, self.avg_y)
            self.firing = False
        
        else: # if less than 2 points (2, not 0, to account for noise and error), assume play pulled trigger, hiding feducal, and fire
            print("FIRE")
            self.firing = True

        # Display the frames with the tracked icons
        #cv2.imshow('Tracked Icon 1', img_matches_icon1)
        #cv2.imshow('Tracked Icon 2', img_matches_icon2)

