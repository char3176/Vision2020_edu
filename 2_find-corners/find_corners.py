import cv2 as cv
import numpy as np
import imutils
import matplotlib.pyplot as plt

img = cv.imread('trapazoid.jpg')
canvas = img.copy()

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

(threshRet, bwimg) = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

(contourRet, contour) = cv.findContours(bwimg, 1, 2)

#      imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
#      ret, thresh = cv.threshold(imgray, 127, 255, 0)
#      contours, hierarchy = cv.findContours(thres, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cnt = contourRet[0]

percentArcLength=0.01
epsilon = percentArcLength*cv.arcLength(cnt, True)
approx = cv.approxPolyDP(cnt, epsilon, True)

#approx = []
#percentArcLength = 1
#while len(approx) != 8:
#    percentArcLength = percentArcLength/2
#    print(percentArcLength)
#    epsilon = percentArcLength*cv.arcLength(cnt, True)
#    approx = cv.approxPolyDP(cnt, epsilon, True)
#    canvas = img.copy()
#    cv.drawContours(canvas, approx, -1, (0, 255, 0), 3)
#    cv.imshow('check len', canvas)
#    cv.waitKey(0)


cv.drawContours(canvas, approx, -1, (0, 255, 0), 3)
cv.imshow('Points', canvas)
cv.waitKey(0)

cv.drawContours(canvas, [approx], -1, (0, 255, 0), 3)
cv.imshow('Contour Approximation', canvas)
cv.waitKey(0)

print(approx)
# Should yield following coords:  array([[[140, 253]], [[194, 346]], [[305, 346]], [[357, 256]], [[344, 257]], [[298, 334]], [[193, 332]], [[151, 255]]], dtype=int32)


#Try "percentArcLength" = 0.1, 0.05, 0.01, 0.001


# get "image moments" from contour
M = cv.moments(cnt)
centroid_x = int(M['m10']/M['m00'])
centroid_y = int(M['m01']/M['m00'])
# Centroid x,y coords should correspond to roughly: 254, 314

# filter to get
