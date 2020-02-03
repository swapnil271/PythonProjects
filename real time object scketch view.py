import cv2
import numpy as np

#sketch generating function
def sketch(image):
    #convert image to grayscale
    img_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #cleaning up the image using Gaussian blur
    img_gray_blur=cv2.GaussianBlur(img_gray,(5,5),0)

    #extract edges

    canny_edges=cv2.Canny(img_gray_blur,10,70)

    #do an invert binarize the image
    ret, mask=cv2.threshold(canny_edges,70,255,cv2.THRESH_BINARY_INV)
    return mask

#initialize webcam, cap is the object provided by video capture
#it contains a Boolean indicating if it was successful(ret)
#it also contains the images collected from the webcam(frame)

cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    cv2.imshow('livesketcher',sketch(frame))
    if cv2.waitKey(1) == 13:    #13 is the enterkey
        break

#release camera and close window, remember to release the webcam with the help of cap.release()
cap.release()
cv2.destroyAllWindows()
