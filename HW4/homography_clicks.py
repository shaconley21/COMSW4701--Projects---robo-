import cv2 
import numpy as np
from picamera import *

pt1 = None
pt2 = None
pt3 = None
pt4 = None
pts_src = None

def point_collection(pt1, pt2, pt3, pt4):
	if event is cv2.EVENT_LBUTTONDOWN:
    	if pt1 is None:
    		pt1 = [x, y]
		elif pt2 is None:
    		pt2 = [x, y]
    	elif pt3 is None:
    		pt3 = [x,y]
    	elif pt4 is None:
    		pt4 = [x,y]

    # Four corners of the book in source image
    pts_src = np.array([pt1, pt2, pt3, pt4])

camera = PiCamera()
camera.resolution = (400,600)
time.sleep(3)
camera.capture('destination.jpg')
im_dst = cv2.imread('destination.jpg')
camera.capture('source.jpg')
im_src = cv2.imread('source.jpg')

#let user select region
cv2.namedWindow('image')
cv2.setMouseCallback('image', point_collection)
cv2.imshow('image', im_src)
print "passed imshow"
cv2.waitKey(6000)
print "passed waitkey"
cv2.destroyAllWindows()


pts_dst = np.array([(0,0),(0, 400), (600, 400), (600,0)])
# Calculate Homography
h, status = cv2.findHomography(pts_src, pts_dst)
     
# Warp source image to destination based on homography
im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
     
# Display images
cv2.imshow("Warped Source Image", im_out)
 
cv2.waitKey(0)


 