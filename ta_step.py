# from gopigo import *
# import picamera
import time
import cv2
import numpy as np
import copy
from math import *

import cStringIO



SECOND_PER_CM = 7.51/100
SECOND_PER_DEGREE = 4.21/360
STOPPING_DISTANCE = 5
pt1 = None
pt2 = None
pt3 = None
pt4 = None
pts_src = None

def point_collection(event, x, y, flags, param):
	global pt1, pt2, pt3, pt4, pts_src
	if event is cv2.EVENT_LBUTTONDOWN:
		if pt1 is None:
			pt1 = [x, y]
		elif pt2 is None:
			pt2 = [x, y]
		elif pt3 is None:
			pt3 = [x,y]
		elif pt4 is None:
			pt4 = [x,y]
	pts_src = np.array([pt1, pt2, pt3, pt4])

def streams():
	# Open a buffer to write the image to memory
	stream = cStringIO.StringIO()
	while True:	  

		# Overwrite any previous information in buffer
		stream.seek(0)
		stream.truncate()

		# Pass buffer to picamera
		yield stream

		# Convert image to CV2 image
		stream.seek(0)
		# Construct a numpy array from the stream
		data = np.fromstring(stream.getvalue(), dtype=np.uint8)
		# "Decode" the image from the array, preserving colour
		image = cv2.imdecode(data, 1)

		# Put any business logic in this function
		process_image(image)

def process_image(image):
	# Do something with the image
	print(image.shape)
	h_matrix, im_out = homography(image)
	robopts = get_roboline_pts(im_out.shape, h_matrix)
	#image_clone = copy.deepcopy(image)
	#cv2.line(image_clone,(road_pt1x,road_pt1y),(road_pt2x,road_pt2y),(255,0,0),2)
	yellowpts = threshough(im_out)

	cv2.line(im_out,(robopts[0][0],robopts[0][1]),(robopts[1][0],robopts[1][1]),(255,0,0),2)
	cv2.imshow("Source Image", im_out)
	cv2.waitKey(2000)
	cv2.destroyAllWindows()

	if len(yellowpts) == 1:
		#do 180 depending on how close to the orange I am
		if yellowpts[0] < STOPPING_DISTANCE:
			move_left(180)
	elif len(yellowpts) == 0:
		#no yellow is seen, turn to see if you can find it
		move_left(30)
	elif len(yellowpts) == 2:
		angle = get_angle(robopts, yellowpts)
		offset, pos = get_dist(robopts, yellowpts)

		#if angle is not 0, turn so that angle is 0
		if angle > 3:
			move_left(angle)
		elif angle < -3:
			move_right(angle)
		else:
			#if angle is 0, offset is 0, go fwd
			#if angle is 0, offset is not 0, turn towards line, go fwd, turn back
			if offset < 20:
				move_fwd(3)
			else:
				if pos == "left":
					move_right(90)
					move_fwd(offset/20)		#going with 100px = 5cm
					move_left(90)
				elif pos == "right":
					move_left(90)
					move_fwd(offset/20)		#going with 100px = 5cm
					move_right(90)
	pass

def homography(image):
	global pts_src
	im_src = image
	pts_dst = np.array([(0,0),(600,0),(600,400),(0,400)])

	
	#calculate homography, warp source image to destination based on homography
	h, status = cv2.findHomography(pts_src, pts_dst)
	im_out = cv2.warpPerspective(im_src, h, (600,400))

	# Display images
	cv2.imshow("Source Image", im_src)
	cv2.imshow("Warped Source Image", im_out)
	cv2.waitKey(2000)
	cv2.destroyAllWindows()
	print ("homography transform matrix:")
	print (h)
	cv2.imwrite("homography_applied.jpg", im_out)
	return h, im_out

def threshough(image):
	image = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
	image_clone = copy.deepcopy(image)
	orange = cv2.inRange(image_clone, np.array([5, 50, 50]), np.array([15, 255, 255]))
	orange_edges= cv2.Canny(orange, 100, 200)
	if len(orange_edges) != 0:
		#calculate distance to orange edge
		print "orange seen!"
		#return [0]
	cv2.imwrite("stop_sign_filtered.jpg", image_clone)
	image = cv2.inRange(image, np.array([90, 100, 100]), np.array([110, 255, 255]))
	edges = cv2.Canny(image, 100, 200)
	if len(edges) == 0:
		print "no yellow seen"
		return []
	lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
	cv2.imwrite("yellow_color_filtered.jpg", image)
	pts = []
	for line in lines:
		rho = line[0][0]
		theta = line[0][1]
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 400*(-b))
		y1 = int(y0 + 400*(a))
		x2 = int(x0 - 400*(-b))
		y2 = int(y0 - 400*(a))
		pts.append((x1, y1))
		pts.append((x2, y2))
		print((x1, y1), (x2, y2))
	midx1 = (pts[0][0] + pts[2][0])/2
	midy1 = (pts[0][1] + pts[2][1])/2
	midx2 = (pts[1][0] + pts[3][0])/2
	midy2 = (pts[1][1] + pts[3][1])/2

	# Display middle of yellow lines line for testing/proof
	#print midx1, midy1, midx2, midy2
	#cv2.line(image,(midx1,midy1),(midx2,midy2),(0,100,255),2)
	cv2.line(image, (pts[2][0],pts[2][1]), (pts[3][0], pts[3][1]), (0, 100,255), 2)
	cv2.line(image, (pts[0][0], pts[0][1]), (pts[1][0], pts[1][1]), (0,100,255),2)	
	cv2.imshow("Source Image", image)
	cv2.waitKey(2000)
	cv2.destroyAllWindows()
	cv2.imwrite("calculated_hough_lines.jpg", image)
	return [(midx1,midy1), (midx2,midy2)]

def get_roboline_pts(shape, transform):
	midx = shape[1]/2
	endy = shape[0]

	#from lab instructions on transforming single points
	source_pt1 = np.array([midx,0,1])
	road_pt1 = transform.dot(source_pt1)
	road_pt1x = int(road_pt1[0]/road_pt1[2])
	road_pt1y = int(road_pt1[1]/road_pt1[2])

	source_pt2 = np.array([midx,endy,1])
	road_pt2 = transform.dot(source_pt2)
	road_pt2x = int(road_pt2[0]/road_pt2[2])
	road_pt2y = int(road_pt2[1]/road_pt2[2])

	return [(road_pt1x,road_pt1y), (road_pt2x,road_pt2y)]

def get_dist(a, b):
	b1 = b[0]
	b2 = b[1]
	b_slope = float((b2[1]-b1[1])/(b2[0]-b1[0]))
	b_yintercept = b1[1] - b_slope*b1[0]
	y = a[0][1]
	x = y*b_slope + b_yintercept
	l_or_r = ""
	if x > a[0][0]:
		#yellowpts' x is greater than robopts' x -> robo is to the left of the yellow line
		l_or_r = "left"
	else:
		l_or_r = "right"

	dist = sqrt((a[0][0]-x)**2 + (y-y)**2)
	print ("Calculated Distance Offset:")
	print (distance)
	return dist, l_or_r

def get_angle(a, b):
	a1 = a[0]
	a2 = a[1]
	b1 = b[0]
	b2 = b[1]
	a_slope = float((a2[1]-a1[1])/(a2[0]-a1[0]))
	b_slope = float((b2[1]-b1[1])/(b2[0]-b1[0]))
	angle = degrees(atan(float((a_slope-b_slope)/(1+a_slope*b_slope))))
	print ("Calculated Angle Offset:")
	print (angle)
	return angle

def move_fwd(cm):
	fwd()
	time.sleep(SECOND_PER_CM*cm)
	stop()
	time.sleep(.2)
def move_right(deg):
	right_rot()
	time.sleep(SECOND_PER_DEGREE*deg)
	stop()
	time.sleep(.2)
def move_left(deg):
	left_rot()
	time.sleep(SECOND_PER_DEGREE*deg)
	stop()
	time.sleep(.2)

def main():
	#servo(83)
	image_width = 400
	image_height = 200

	# with picamera.PiCamera() as camera:
	# 	camera.resolution = (image_width, image_height)
	# 	time.sleep(3)
	# 	camera.capture('source.jpg')
	# 	image = cv2.imread('source.jpg')

	if True:
		im_dst = cv2.imread('homography_calibration.jpg')	
		#let user select region
		cv2.namedWindow('clickme4x')
		cv2.setMouseCallback('clickme4x', point_collection)
		cv2.imshow('clickme4x', im_dst)
		print "passed imshow"
		cv2.waitKey(6000)
		print "passed waitkey"
		cv2.destroyAllWindows()
		print pts_src
		# h_matrix = homography(image)

		# camera.capture('source.jpg')
		image = cv2.imread('original_image.jpg')
		process_image(image)



	# with picamera.PiCamera() as camera:
	# 	# Set resolution of camera and the framerate
	# 	# A higher fps won't necessarily result in faster images
	#	 camera.resolution = (image_width, image_height)
	#	 camera.framerate = 30
	#	 camera.capture_sequence(streams(), use_video_port=True)


if __name__ == "__main__":
	main()
