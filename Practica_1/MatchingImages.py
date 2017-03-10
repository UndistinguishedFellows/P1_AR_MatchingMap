# Aliex Cardona and Josep Casanovas
# Realitat aumentada practica 1

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PyFiles.convolutionKernel import applyKernel

IMAGES_PATH = "../Images/"

#imageName = IMAGES_PATH + input("Source image: ")
#targetName = IMAGES_PATH + input("Target to search: ")
#detectionThreshold = input("Detection threshold: ")

imageName = IMAGES_PATH+'img1.png'
targetName = IMAGES_PATH+'t1-img1.png'

img = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)
template = cv2.imread(targetName, cv2.IMREAD_GRAYSCALE)

res = cv2.matchTemplate(img,template,0)

plt.subplot(1,1,1), plt.imshow(res, cmap = 'gray')
plt.title('Matching map'), plt.xticks([]), plt.yticks([])
plt.show()