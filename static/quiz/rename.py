import os

formats = ['.jpg', '.png', '.jpeg']
images = os.listdir()

c = 0
for img in images:
	if os.path.splitext(img) in formats:
		os.rename(img, img.replace('_', '%'))
		c += 1

print('%d files renamed' % c)