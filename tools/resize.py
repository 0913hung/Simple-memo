from PIL import Image

image_list=["del.png","bigger.png","smaller.png","new.png","save.png","close.png"]

for i in image_list:
	img = Image.open(i)
	width, height = img.size
	img = img.resize((15, 15), Image.ANTIALIAS)
	img.save(i, format='PNG')