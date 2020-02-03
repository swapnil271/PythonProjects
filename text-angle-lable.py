
import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import pytesseract 

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

src_path = r"C:\Users\DELL\Desktop\tractor\IMG_20190125_093806.jpg"

#1.1 : code for extract the image text

img = cv2.imread(src_path)

# Apply dilation and erosion to remove some noise
kernel = np.ones((1, 1), np.uint8)
img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)

# Write the image after apply opencv to do some ...
cv2.imwrite(src_path + "thres.png", img)

# Recognize text with tesseract for python
result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))

print ('--- Start recognize text from image ---')
print (result)


#1.2 : code for angle of the image text

def detect_angle(image):
    mask = np.zeros(image.shape, dtype=np.uint8)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    adaptive = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,15,4)

    cnts = cv2.findContours(adaptive, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        area = cv2.contourArea(c)
        if area < 45000 and area > 20:
            cv2.drawContours(mask, [c], -1, (255,255,255), -1)

    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    h, w = mask.shape

    # Horizontal
    if w > h:
        left = mask[0:h, 0:0+w//2]
        right = mask[0:h, w//2:]
        left_pixels = cv2.countNonZero(left)
        right_pixels = cv2.countNonZero(right)
        return 0 if left_pixels >= right_pixels else 180
    # Vertical
    else:
        top = mask[0:h//2, 0:w]
        bottom = mask[h//2:, 0:w]
        top_pixels = cv2.countNonZero(top)
        bottom_pixels = cv2.countNonZero(bottom)
        return 90 if bottom_pixels >= top_pixels else 270

if __name__ == '__main__':
    image = cv2.imread(src_path)
    angle = detect_angle(image)
    print(angle)



#1.3 : code for Lebling


def resize_image(event):
    new_width = event.width
    new_height = event.height

    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)

    label.config(image=photo)
    label.image = photo  # avoid garbage collection

root = Tk()
root.title("Title")
root.geometry('600x600')

frame = Frame(root, relief='raised', borderwidth=2)
frame.pack(fill=BOTH, expand=YES)
frame.pack_propagate(False)



copy_of_image = Image.open(src_path)
photo = ImageTk.PhotoImage(copy_of_image)

label = Label(frame, image=photo)
label.place(x=0, y=0, relwidth=1, relheight=1)
label.bind('<Configure>', resize_image)

bottom_frame = Frame(frame, relief='raised', borderwidth=2)
bottom_frame.place(relx=0.5, rely=0.94, anchor=CENTER)

#Lable First
Label(bottom_frame, text='Name : '+ result, width=60).pack()

#Lable Second
Label(bottom_frame, text='Angle : '+ str(angle), width=60).pack()


root.mainloop()
