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
            pixelResult += pow((int((originalImage[matchingMapPosX + i][matchingMapPosY + j]) - int(targetImage[i][j]))), 2)

    return pixelResult

#----------------------------------------------------------
#Loading images.

"""imageName = input("Source image: ")
targetName = input("TargetImage: ")
detectionThreshold = input("Detection threshold: ")"""
imageName = "img3.jpg"
targetName = "t1-img3.jpg"
detectionThreshold = 0.1

originalImage = cv2.imread(IMAGES_PATH + imageName, cv2.IMREAD_GRAYSCALE)
targetImage = cv2.imread(IMAGES_PATH + targetName, cv2.IMREAD_GRAYSCALE)

originalImageColor = cv2.imread(IMAGES_PATH + imageName, cv2.IMREAD_COLOR)
targetImageColor = cv2.imread(IMAGES_PATH + targetName, cv2.IMREAD_COLOR)

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
if minValue / maxValue <= detectionThreshold:
    for i in range(0, matchingMap.shape[0]):
        for j in range(0, matchingMap.shape[1]):
            if matchingMap[i][j] == minValue:
                matchings.append((j, i))  #NOTE: If i append i, j cords are wrong. Cant understand why

numOfMatches = len(matchings)

print "Num of matching points: " + str(numOfMatches)

#Create a black image and set the font
imgFound = np.zeros((40, 320, 3), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX

if numOfMatches > 0:
    cv2.putText(imgFound, "TARGETS FOUND: " + str(numOfMatches), (5, 30), font, 1, (0, 255, 0), 2)
    for n in range(0, len(matchings)):
        print "Point " + str(n) +": " + str(matchings[n][0]) + ", " + str(matchings[n][1])
        matchingPoint = (matchings[n][0] + targetImageSize[0] / 2, matchings[n][1] + targetImageSize[1] / 2)
        cv2.rectangle(originalImageColor, (matchings[n][0], matchings[n][1]), (matchingPoint[0] + targetImage.shape[1] / 2, matchingPoint[1] + targetImage.shape[0] / 2), 0, 2) #Here with target size have the same issue as before. Have switched the size between x and y...

else:
    cv2.putText(imgFound, "TARGET NOT FOUND", (5, 30), font, 1, (255, 0, 0), 2)
    print "No matches."

#Normalize before showing the image
for i in range(0, matchingMap.shape[0]):
    for j in range(0, matchingMap.shape[1]):
        matchingMap[i][j] = matchingMap[i][j] / maxValue


cv2.imshow("Result", imgFound)
cv2.imshow("Original image: " + imageName, originalImageColor)
cv2.imshow("Target image: " + targetName, targetImageColor)

cv2.imshow("Matching map", matchingMap)

#----------------------------------------------------------

k = cv2.waitKey(0)

if k == 27:
    cv2.destroyAllWindows()

