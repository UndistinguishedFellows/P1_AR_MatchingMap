#Realitat aumentada. Practica 1. CITM(UPC)
#Aleix Cardona
#Josep Casanovas
#Github: https://github.com/UndistinguishedFellows/RealitatAumentadaPractiques

import cv2
import numpy as np


#----------------------------------------------------------
#CONSTATNS:
IMAGES_PATH = "../Images/"

#----------------------------------------------------------
#FUNCTIONS:

def getMatchingMapPixelValue(matchingMapPosX, matchingMapPosY, originalImage, targetImage):
    pixelResult = 0

    #To calc the pixel we must iterate the target image and sum all the values with the wanted section of the image

    for i in range(0, targetImage.shape[0]):
        for j in range(0, targetImage.shape[1]):
            pixelResult += pow((int(targetImage[i][j]) - int((originalImage[matchingMapPosX + i][matchingMapPosY + j]))), 2)

    return pixelResult

#----------------------------------------------------------
#Loading images.

if input("Default image path is: " + IMAGES_PATH + "\nDo you want to change it? (y/n): ") == "y":
    IMAGES_PATH = input("New images path: ")

imageName = input("Source image: ")
targetName = input("TargetImage: ")
detectionThreshold = input("Detection threshold: ")

"""imageName = "img1.png"
targetName = "t2-img1.png"
detectionThreshold = 0.1"""

scale = 1

if input("For optimitzation purposes we can resize the images in order to speed up the search, by default scale is 1.\nIf you rescale the image a false positive might be found, do this at your own risk. \nDo you want to change the scale? (y/n):" ) == "y":
    scale = input("Scale: ")

sclRatio = 1/scale

originalImageColor = cv2.imread(IMAGES_PATH + imageName, cv2.IMREAD_COLOR)
targetImageColor = cv2.imread(IMAGES_PATH + targetName, cv2.IMREAD_COLOR)

#Once images are loaded check if target dimensions are fine.
if originalImageColor.shape[0] < targetImageColor.shape[0] or originalImageColor.shape[1] < targetImageColor.shape[1]:
    print "ERROR: Target image is bigger than original image."
    exit()

originalImageBig = cv2.imread(IMAGES_PATH + imageName, cv2.IMREAD_GRAYSCALE)
targetImageBig = cv2.imread(IMAGES_PATH + targetName, cv2.IMREAD_GRAYSCALE)

originalImage = cv2.resize(originalImageBig, (0, 0), fx=scale, fy=scale)
targetImage = cv2.resize(targetImageBig, (0, 0), fx=scale, fy=scale)

#----------------------------------------------------------
#Actually calculating matching map.

originalImageSize = originalImage.shape
targetImageSize = targetImage.shape
matchingMapSize = (originalImageSize[0] - targetImageSize[0] + 1, originalImageSize[1] - targetImageSize[1] + 1)

matchingMap = np.zeros(shape=(matchingMapSize))

for i in range(0, matchingMapSize[0]):
    for j in range(0, matchingMapSize[1]):
        matchingMap[i][j] = getMatchingMapPixelValue(i, j, originalImage, targetImage)

#Detect all matching points
maxValue = matchingMap.max()
minValue = matchingMap.min()
matchings = []
if (minValue / maxValue) <= detectionThreshold:
    for i in range(0, matchingMap.shape[0]):
        for j in range(0, matchingMap.shape[1]):
            if matchingMap[i][j] == minValue:
                matchings.append((int(j*sclRatio), int(i*sclRatio)))  #NOTE: If i append i, j cords are wrong. Cant understand why

numOfMatches = len(matchings)

print "Num of matching points: " + str(numOfMatches)

#Create a black image and set the font
imgFound = np.zeros((40, 320, 3), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX

if numOfMatches > 0:
    cv2.putText(imgFound, "TARGETS FOUND: " + str(numOfMatches), (5, 30), font, 1, (0, 255, 0), 2)
    for n in range(0, len(matchings)):
        print "Point " + str(n) +": " + str(matchings[n][0]) + ", " + str(matchings[n][1])
        cv2.rectangle(originalImageColor, (matchings[n][0], matchings[n][1]), (matchings[n][0] + targetImageBig.shape[1], matchings[n][1] + targetImageBig.shape[0]), 0, 2)

else:
    cv2.putText(imgFound, "TARGET NOT FOUND", (5, 30), font, 1, (255, 0, 0), 2)
    print "No matches."

#Normalize before showing the image
for i in range(0, matchingMap.shape[0]):
    for j in range(0, matchingMap.shape[1]):
        matchingMap[i][j] = matchingMap[i][j] / maxValue


#----------------------------------------------------------
#Display

cv2.imshow("Original image: " + imageName, originalImageColor)
cv2.imshow("Target image: " + targetName, targetImageColor)
cv2.imshow("Matching map", matchingMap)

cv2.imshow("Result", imgFound)


k = cv2.waitKey(0)

if k == 27:
    cv2.destroyAllWindows()

