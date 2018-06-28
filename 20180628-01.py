"""
Image thumbnail test

Ref:
	https://stackoverflow.com/questions/2612436/create-thumbnail-images-for-jpegs-with-python
	https://stackoverflow.com/questions/1386352/pil-thumbnail-and-end-up-with-a-square-image

"""
from PIL import Image
size = (36, 36)
data = "test22222.png"
image = Image.open(data)
image.thumbnail(size, Image.ANTIALIAS)
background = Image.new('RGBA', size, (255, 255, 255, 0))
background.paste(
    image, (int((size[0] - image.size[0]) / 2), int((size[1] - image.size[1]) / 2))
)
background.save("output.png")