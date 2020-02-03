import re
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


img_path = r"C:\Users\DELL\Desktop\M.Tech\ISRO_Payment.png"
im = cv2.imread(img_path)
newdata = pytesseract.image_to_osd(im, nice=1)
re.search('(?<=Rotate: )\d+', newdata).group(0)
