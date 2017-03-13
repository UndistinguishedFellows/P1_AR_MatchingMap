import sys
import math
import numpy as np
import cv2


# Function that returns 
def applyKernel(posX, posY, inputImg, kernel):

    pixelValue = 0.0

    rK, cK = kernel.shape
    r, c = inputImg.shape
    limitRows = int(rK/2)
    limitCols = int(cK/2)

    for i in range(-limitRows, limitRows+1):
        for j in range(-limitCols, limitCols+1):
            if posX + i >= 0 and posX + i < r and posY + j >= 0 and posY + j < c:
                pixelValue += inputImg[posX + i][posY + j] * kernel[i + limitRows][j + limitCols]

    return pixelValue

def squaredDifference(posX, posY, input_image, target_image):

    pixel_value = 0.0

    rT, cT = target_image.shape
    r, c = input_image.shape
    matching_map_res = (r - rT + 1, c - cT + 1)

    #limitRows = int(matching_map_res[0] / 2)
    #limitCols = int(matching_map_res[1] / 2)
    limitRows = int(rT / 2)
    limitCols = int(cT / 2)

    for i in range(-limitRows, limitRows+1):
        for j in range(-limitCols, limitCols+1):
            #if posX+i >= 0 and posX+i < r and posY+j >=0 and posY+j < c:
            pixel_value += pow((target_image[limitRows + i][limitCols + j] - input_image[posX + i][posY + j]), 2)
            #print pixel_value

    return pixel_value

def getMatchingMap(input_image, target_image):

    rT, cT = target_image.shape
    r, c = input_image.shape
    matching_map_res = (r - rT + 1, c - cT + 1)

    matching_map = np.zeros(shape=(matching_map_res[0], matching_map_res[1]))
    limitRows = int(matching_map_res[0] / 2)
    limitCols = int(matching_map_res[1] / 2)

    for i in range(-limitRows, limitRows):
        for j in range(-limitCols, limitCols):
            matching_map[i + limitRows][j + limitCols] = squaredDifference(i + limitRows, j + limitCols, input_image , target_image)
    return matching_map

'''
# Read input image in grayscale
filename = input("Introduce Image: ")
img = cv2.imread(filename, 0)
rows, cols = img.shape


# Images to store the filtered images
GX = np.zeros((rows, cols))
GY = np.zeros((rows, cols))
G = np.zeros((rows, cols))
boxOutput = np.zeros((rows, cols))


# Kernels to use
sobelX = np.array([[-1.0, 0.0, 1.0],
                   [-2.0, 0.0, 2.0],
                   [-1.0, 0.0, 1.0]])

sobelY = np.array([[-1.0, -2.0, -1.0],
                   [0.0, 0.0, 0.0],
                   [1.0, 2.0, 1.0]])

boxFilter = np.array([[0.04, 0.04, 0.04, 0.04, 0.04],
                      [0.04, 0.04, 0.04, 0.04, 0.04],
                      [0.04, 0.04, 0.04, 0.04, 0.04],
                      [0.04, 0.04, 0.04, 0.04, 0.04],
                      [0.04, 0.04, 0.04, 0.04, 0.04]])


# To normalize, we need to compute the maximum values of the filtered images
# We initialize these values with the minimum value that can be stored in an integer
maximumGX = -sys.maxint
maximumGY = -sys.maxint
maximumG = -sys.maxint
maximumBF = -sys.maxint


# Compute the filtered images
for i in range(0, rows):
    for j in range(0, cols):
        GX[i][j] = abs(applyKernel(i, j, img, sobelX))
        GY[i][j] = abs(applyKernel(i, j, img, sobelY))
        G[i][j] = np.sqrt(GX[i][j]**2+GY[i][j]**2)
        boxOutput[i][j] = applyKernel(i, j, img, boxFilter)

        if GX[i][j] > maximumGX:
            maximumGX = GX[i][j]
        if GY[i][j] > maximumGY:
            maximumGY = GY[i][j]
        if G[i][j] > maximumG:
            maximumG = G[i][j]
        if boxOutput[i][j] > maximumBF:
            maximumBF = boxOutput[i][j]

#Normalize to show using cv2.imshow (values in range [0.0, 1.0])
for i in range(0, rows):
    for j in range(0, cols):
        GX[i][j] = GX[i][j]/maximumGX
        GY[i][j] = GY[i][j]/maximumGY
        G[i][j] = G[i][j]/maximumG
        boxOutput[i][j] = boxOutput[i][j]/maximumBF

# Show the results in separated windows
cv2.imshow("Image grayscale", img)
cv2.imshow("Sobel X", GX)
cv2.imshow("Sobel Y", GY)
cv2.imshow("Gradient magnitude", G)
cv2.imshow("Box Filter", boxOutput)

# Wait till a key is pressed
key = cv2.waitKey(0)

# Quit when the key 'q' is pressed
while key != ord('q'): 
    key = cv2.waitKey(0)
else:
    cv2.destroyAllWindows()
'''