import cv2
import numpy as np
import pytesseract
from PIL import Image
print ("Hello")
src_path = r"C:\Users\DELL\Desktop\Master_Image\temp.jpg"

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


print (src_path)


# Read image with opencv
img = cv2.imread(src_path)

# Convert to gray
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Apply dilation and erosion to remove some noise
kernel = np.ones((1, 1), np.uint8)

img = cv2.resize(img, None, fx=0.3, fy=0.29005, interpolation = cv2.INTER_AREA)

img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)



# Write image after removed noise
#cv2.imwrite(src_path + "removed_noise.png", img)

#  Apply threshold to get image with only black and white
#img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

# Write the image after apply opencv to do some ...
cv2.imwrite(src_path + "thres.png", img)

# Recognize text with tesseract for python
result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))


# Remove template file
#os.remove(temp)


print ('--- Start recognize text from image ---')
print (result)

import tkinter as tk

# if you are still working under a Python 2 version, 
# comment out the previous line and uncomment the following line
# import Tkinter as tk

root = tk.Tk()

w = tk.Label(root, text=result)
w.pack()

root.mainloop()
