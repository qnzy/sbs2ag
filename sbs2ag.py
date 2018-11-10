import numpy as np
import sys
import cv2

if len(sys.argv) != 2:
    print('give input video as command line argument')

videoName = sys.argv[1]
videoIn = cv2.VideoCapture(videoName)
fourcc   = cv2.VideoWriter_fourcc(*'MJPG')

fps    = round(videoIn.get(cv2.CAP_PROP_FPS))
width  = round(videoIn.get(cv2.CAP_PROP_FRAME_WIDTH))
height = round(videoIn.get(cv2.CAP_PROP_FRAME_HEIGHT))

#print(f'{width}x{height} {fps}fps')

videoOut = cv2.VideoWriter('output.avi', fourcc, fps, (width//2, height))

while (videoIn.isOpened()):
    ret, frame = videoIn.read()
    if frame is  None:
        break
    h,w,c = frame.shape
    anagl = np.zeros((h, w//2, 3)).astype(np.uint8)
    if c != 3:
        print('error: should be 3 channel frames')
    if w != width:
        print('error: wrong frame width')
    left = frame[:,:w//2,:]
    right = frame[:,w//2:,:]
    # 0: b, 1: g, 2: r
    anagl[:,:,0] = right[:,:,0]
    anagl[:,:,1] = right[:,:,1]
    anagl[:,:,2] = left[:,:,2]
    videoOut.write(anagl)

videoIn.release()
videoOut.release()
cv2.destroyAllWindows()

