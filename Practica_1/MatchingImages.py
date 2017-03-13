# Aliex Cardona and Josep Casanovas
# Realitat aumentada practica 1

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PyFiles.convolutionKernel import getMatchingMap

IMAGES_PATH = "../Images/"

#imageName = IMAGES_PATH + input("Source image: ")
#targetName = IMAGES_PATH + input("Target to search: ")
#detectionThreshold = input("Detection threshold: ")

imageName = IMAGES_PATH+'img1.png'
targetName = IMAGES_PATH+'t1-img1.png'

img = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)
template = cv2.imread(targetName, cv2.IMREAD_GRAYSCALE)

res = cv2.matchTemplate(img,template,0)
matching_map = getMatchingMap(img, template)

min_value_X = 0
min_value_Y = 0
min_value = 255

for i in range(matching_map.shape[0]):
    for j in range(matching_map.shape[1]):
        if matching_map[i][j] < min_value:
            min_value = matching_map[i][j]
            min_value_X = j
            min_value_Y = i

cv2.rectangle(img,(min_value_X - 6, min_value_Y - 6), (min_value_X + 6, min_value_Y + 6), 0, 2)



print img.shape
print template.shape
print res.shape
print matching_map.shape



plt.subplot(1,3,1), plt.imshow(res, cmap = 'gray')
plt.title('Matching map'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,2), plt.imshow(matching_map, cmap = 'gray')
plt.title('Matching map'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,3), plt.imshow(img, cmap = 'gray')
plt.title('Matching map'), plt.xticks([]), plt.yticks([])
plt.show()