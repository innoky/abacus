import re
import cv2
import pytesseract as tess


png = "test.png"
text = tess.image_to_string(png)
text.replace(" ", "")
pattern = re.compile("([0-9][=+-/*])")
equations = [x for x in text if bool(re.match(pattern, x))]

print(re.findall(r'(.*)', str(text))[0])
