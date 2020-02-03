import cv2
import numpy as np

# Create our body classifier
body_classifier = cv2.CascadeClassifier(r'C:\Users\DELL\Desktop\Data Framing\haarcascade_fullbody.xml')

# Initiate video capture for video file, here we are using the video file in which pedestrians would be detected
cap = cv2.VideoCapture(r'C:\Users\DELL\Desktop\Data Framing\pedestrians_road_city_cars_traffic_1040.mp4')

# Loop once video is successfully loaded
while cap.isOpened():

    # Reading the each frame of the video 
    ret, frame = cap.read()

  # here we are resizing the frame, to half of its size, we are doing to speed up the classification
 # as larger images have lot more windows to slide over, so in overall we reducing the resolution
#of video by half that’s what 0.5 indicate, and we are also using quicker interpolation method that is #interlinear
    frame = cv2.resize(frame, None,fx=0.4, fy=0.4, interpolation = cv2.INTER_LINEAR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Pass frame to our body classifier
    bodies = body_classifier.detectMultiScale(gray, 1.2, 3)

    # Extract bounding boxes for any bodies identified
    for (x,y,w,h) in bodies:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.imshow('Pedestrians', frame)

    if cv2.waitKey(1) == 20: #13 is the Enter Key
        break

cap.release()
cv2.destroyAllWindows()
