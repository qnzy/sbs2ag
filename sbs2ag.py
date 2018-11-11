from __future__ import print_function
import sys
import numpy as np
import cv2

if len(sys.argv) != 2:
    print('give input video as command line argument')

videoName  = sys.argv[1]
videoIn    = cv2.VideoCapture(videoName)
fps        = int(videoIn.get(cv2.CAP_PROP_FPS))
width      = int(videoIn.get(cv2.CAP_PROP_FRAME_WIDTH))
height     = int(videoIn.get(cv2.CAP_PROP_FRAME_HEIGHT))
frameCount = int(videoIn.get(cv2.CAP_PROP_FRAME_COUNT))
fourcc     = cv2.VideoWriter_fourcc(*'MJPG')
#fourcc     = int(videoIn.get(cv2.CAP_PROP_FOURCC))
videoOut   = cv2.VideoWriter('output.avi', fourcc, fps, (width//2, height))

anagl = np.zeros((height, width//2, 3)).astype(np.uint8)
currentFrame = 0
frameProgress = 0
print('converting: ', end='')
sys.stdout.flush()
while (videoIn.isOpened()):
    ret, frame = videoIn.read()
    if frame is  None:
        break
    h,w,c = frame.shape
    if w != width or h != height or c != 3:
        print('frame dimension error')
        break
    currentFrame += 1
    if currentFrame - frameProgress >= frameCount/10:
        print('.', end='')
        sys.stdout.flush()
        frameProgress = currentFrame
    left = frame[:,:w//2,:]
    right = frame[:,w//2:,:]
    # 0: b, 1: g, 2: r
    anagl[:,:,0] = right[:,:,0]
    anagl[:,:,1] = right[:,:,1]
    anagl[:,:,2] = left[:,:,2]
    videoOut.write(anagl)
print('done')

videoIn.release()
videoOut.release()

