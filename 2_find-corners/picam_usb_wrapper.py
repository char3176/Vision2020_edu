import os
from imutils.video import VideoStream
import numpy as np
import datetime
import argparse
import imutils
import time
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=1, help="whether or not the Raspi camera should be used")
args = vars(ap.parse_args())

pathToSavedImages = "/home/pi/data-images"
CHECK_FOLDER = os.path.isdir(pathToSavedImages)
if not CHECK_FOLDER: 
    os.makedirs(pathToSavedImages)
    print("Created dir: ", pathToSavedImages)
else:
    print(pathToSavedImages," directory already exists.")

vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240), framerate=60).start()
time.sleep(2.0)

hsv_green_lower = np.array([0,220,25])
hsv_green_upper = np.array([101, 255, 255])
percentArcLength=0.1

while True:
  frame = vs.read()
  frame = imutils.resize(frame, width=400)
  gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  #####################
  # hsv = cv.cvtColor(frame, cv2.COLOR_BGR2HSV)
  # mask = cv2.inRange(hsv, hsv_green_lower, hsv_green_upper)
  #####################
  (threshRet, mask) = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
  (contourRet, contour) = cv.findContours(mask, 1, 2)
  try: 
    cnt = contourRet[0]
    epsilon = percentArcLength*cv.arcLength(cnt, True)
    approx = cv.approxPolyDP(cnt, epsilon, True)
    ##########################
    #rect = cv.minAreaRect(cnt)
    #approx = cv.boxPoints(rect)
    ##approx = np.int0(approx)
    ##########################
    cv.drawContours(frame, [approx], -1, (0, 0, 255), 3)
    cv.drawContours(frame, approx, -1, (0, 0, 255), 3)
  except IndexError:
    cnt = 'null'
  timestamp = datetime.datetime.now()
  ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
  brightnessContrastSaturationStr = str(vs.camera.brightness) + " / " + str(vs.camera.contrast) + " / " + str(vs.camera.saturation)
  if cnt != "null": 
      fittingStr = str(len(approx)) + " / " + str(percentArcLength)
  else:
      fittingStr = "ERROR: cnt -> list index out of range.  No contour found"
  cv.putText(frame, ts, (10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
  cv.putText(frame, brightnessContrastSaturationStr, (10, frame.shape[0] - 20), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
  cv.putText(frame, fittingStr, (10, frame.shape[0] - 30), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
  cv.imshow("Frame", frame)
  key = cv.waitKey(1) & 0xFF
  if key == ord("q"):
    break
  elif key == ord("w"):
    vs.camera.brightness = min(vs.camera.brightness + 1, 100)
  elif key == ord("s"):
    vs.camera.brightness = max(vs.camera.brightness - 1, 0)
  elif key == ord("x"):
    vs.camera.brightness = 50
  elif key == ord("e"):
    vs.camera.contrast = min(vs.camera.contrast + 1, 100)
  elif key == ord("d"):
    vs.camera.contrast = max(vs.camera.contrast - 1, -100)
  elif key == ord("c"):
    vs.camera.contrast = 0
  elif key == ord("r"):
    vs.camera.saturation = min(vs.camera.saturation + 1, 100)
  elif key == ord("f"):
    vs.camera.saturation = max(vs.camera.saturation - 1, -100)
  elif key == ord("v"):
    vs.camera.saturation = 0
  elif key == ord("u"): 
    percentArcLength = percentArcLength * 2.0
  elif key == ord("j"):
    percentArcLength = percentArcLength / 2.0
  elif key == ord("m"):
    percentArcLength = 0.1
  elif key == ord("p"):
      filetimestamp = timestamp.strftime("%Y%m%d-%H%M%S")
      fileBrightnessContrastSaturation = str(vs.camera.brightness)+"-"+str(vs.camera.contrast)+"-"+str(vs.camera.saturation)
      fileApproxPoints = str(len(approx))
      myFilename = pathToSavedImages+"/"+filetimestamp+"_"+fileBrightnessContrastSaturation+"_"+fileApproxPoints+".jpg"
      print(myFilename)
      cv.imwrite(myFilename,frame)



cv.destroyAllWindows()
vs.stop()
