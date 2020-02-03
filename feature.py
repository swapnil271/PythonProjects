import numpy as np
import cv2
from matplotlib import pyplot as plt
from tkinter import *
from PIL import Image, ImageTk
import tensorflow


Master_image = r"C:\Users\DELL\Desktop\Master_Image\temp.jpg"
New_image = r"C:\Users\DELL\Desktop\tractor\IMG_20190125_093801.jpg"

img1 = cv2.imread(Master_image,0)          # queryImage
img2 = cv2.imread(New_image,0)             # trainImage

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 1
MIN_MATCH_COUNT = 60
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
good = []

good_1 = []
for m,n in matches:
    if m.distance < 0.5*n.distance:
        good.append(m)

for m1,n1 in matches:
    if m1.distance < 0.5*n1.distance:
        good_1.append([m1])
        a=len(good_1)
        percent=(a*100)/len(kp2)
print("{} % similarity".format(percent))

       
if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()
    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)
    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None
draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)
img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
##plt.imshow(img3, 'gray'),plt.show()
cv2.waitKey(1)

############################ Two Image Marge with Lable ###########################

#Read First Image
imgBGR=cv2.imread(Master_image)
imgBGR=cv2.resize(imgBGR,(860,640))
#Read Second Image
imgRGB=cv2.imread(New_image)
imgRGB=cv2.resize(imgRGB,(860,640))


img_concate_Hori=np.concatenate((imgBGR,imgRGB),axis=1)



def resize_image(event):
    new_width = event.width
    new_height = event.height

    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)

    label.config(image=photo)
    label.image = photo  # avoid garbage collection

root = Tk()
root.title("Title")
##root.geometry('1200x750')


RWidth=root.winfo_screenwidth()
RHeight=root.winfo_screenheight()
root.geometry("%dx%d"%(RWidth,RHeight))


frame = Frame(root, relief='raised', borderwidth=2)
frame.pack(fill=BOTH, expand=YES)
frame.pack_propagate(False)

copy_of_image = Image.fromarray(img_concate_Hori)
photo = ImageTk.PhotoImage(copy_of_image)

label = Label(frame, image=photo)
label.place(x=0, y=0, relwidth=1, relheight=1)
label.bind('<Configure>', resize_image)

bottom_frame = Frame(frame, relief='raised', borderwidth=2)
bottom_frame.place(relx=0.5, rely=0.9, anchor=CENTER)

#Lable First
#Label(bottom_frame, text='Model is : ', width=60).pack()
if percent >= 0.3061:
    Label(bottom_frame, text='Match found ',font='Helvetica 18 bold', width=60).pack()
else:
    Label(bottom_frame, text='Not Match found ',font='Helvetica 18 bold', width=60).pack()

root.mainloop()


