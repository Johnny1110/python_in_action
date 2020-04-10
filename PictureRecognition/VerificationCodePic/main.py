import pytesseract as pt

from PIL import Image

image = Image.open('django.jpg')
result = pt.image_to_string(image)
print(result)