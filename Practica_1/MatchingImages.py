# Aliex Cardona and Josep Casanovas
# Realitat aumentada practica 1

import cv2

IMAGES_PATH = "../Images/"

imageName = IMAGES_PATH + input("Source image: ")
targetName = IMAGES_PATH + input("Target to search: ")
detectionThreshold = input("Detection threshold: ")

originalImage = cv2.imread(imageName, cv2.IMREAD_COLOR)
targetImage = cv2.imread(targetName, cv2.IMREAD_COLOR)

cv2.imshow("Original image: " + imageName, originalImage)
cv2.imshow("Target image: " + targetName, targetImage)

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()