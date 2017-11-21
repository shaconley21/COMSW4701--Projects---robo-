#import gopigo
#import picamera
import cv2
import time
import cStringIO
import numpy as np
import copy
from gopigo import *

THREECM = 0
SECOND_PER_DEGREE = 0
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
	h_matrix = homography(image)
	robopts = get_roboline_pts(image.shape, h_matrix)
	yellowpts = threshough(image)
	if lens(val) == 0:
		if dist<distance_to_stop:
			stop()
			time.sleep(0.2)
			left_rot(180)
			time.sleep(0.2)
		#do 180 depending on how close to the orange I am
	elif lens(val) == 1:
		#turn a bit to try and find the yellow line
	elif lens(val) == 2:
		angle = get_angle(robopts, yellowpts)
		offset = get_dist(robopts, yellowpts)
		if angle != 0:
			move_left()
		else:
			if offset == 0:
				move_fwd()
			else:
				move_left()
				move_fwd()
				backward += 1
				dist = right_rot_stop()
				stop()
				time.sleep(1)
		#if angle is not 0, turn so that angle is 0
		#if angle is 0, offset is 0, go fwd
		#if angle is 0, offset is not 0, turn towards line, go fwd, turn back
	pass

def homography(image):
	im_src = image
	pts_dst = np.array([(0,0),(1000,0),(1000,600),(0,600)])

	
	#calculate homography, warp source image to destination based on homography
	h, status = cv2.findHomography(pts_src, pts_dst)
	im_out = cv2.warpPerspective(im_src, h, (1000,600))
	 
	# Display images
	cv2.imshow("Source Image", im_src)
	cv2.imshow("Warped Source Image", im_out)
 
	cv2.waitKey(6000)
	cv2.destroyAllWindows()

	return h

def threshough(image):
	image = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
	image_clone = copy.deepcopy(image)
	orange = cv2.inRange(image_clone, np.array([5, 50, 50]), np.array([15, 255, 255]))
	orange_edges= cv2.Canny(orange, 100, 200)
	if len(orange_edges) != 0:
		return []
	image = cv2.inRange(image, np.array([90, 100, 100]), np.array([110, 255, 255]))
	edges = cv2.Canny(image, 100, 200)
	if len(edges) == 0:
		return [0]
	lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

	pts = []
	for line in lines:
		rho = line[0][0]
		theta = line[0][1]
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))
		pts.append((x1, y1))
		pts.append((x2, y2))
		print((x1, y1), (x2, y2))
	midx1 = (pts[0][0] + pts[2][0])/2
	midy1 = (pts[0][1] + pts[2][1])/2
	midx2 = (pts[1][0] + pts[3][0])/2
	midy2 = (pts[1][1] + pts[3][1])/2
	return [(midx1,midy1), (midx2,midy2)]

def get_center_pts(shape, transform):
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

def get_dist(a, b):
	b1 = b[0]
	b2 = b[1]
	b_slope = float((b2[1]-b1[1])/(b2[0]-b1[0]))
	b_yintercept = b1[1] - b_slope*b1[0]
	y = a[0][1]
	x = y*b_slope + b_yintercept

	dist = sqrt((a[0][0]-x)**2 + (y-y)**2)
	return dist

def get_angle(a, b):
	a1 = a[0]
	a2 = a[1]
	b1 = b[0]
	b2 = b[1]
	a_slope = float((a2[1]-a1[1])/(a2[0]-a1[0]))
	b_slope = float((b2[1]-b1[1])/(b2[0]-b1[0]))
	angle = atan(float((a_slope-b_slope)/(1+a_slope*b_slope)))
	return angle

# def move_fwd():
# 	fwd()
# 	time.sleep(THREECM)
# 	stop()
# 	time.sleep(.2)
# def move_right(deg):
# 	right_rot()
# 	time.sleep(SECOND_PER_DEGREE*deg)
# 	stop()
# 	time.sleep(.2)
# def move_left(deg):
# 	left_rot()
# 	time.sleep(SECOND_PER_DEGREE*deg)
# 	stop()
# 	time.sleep(.2)

def main():
	set_speed(100)

	image_width = 400
	image_height = 600

  #   with picamera.PiCamera() as camera:
  #	   camera.resolution = (image_width, image_height)
		# time.sleep(3)
		# camera.capture('destination.jpg')
		# im_dst = cv2.imread('destination.jpg')
		# camera.capture('source.jpg')
		# im_src = cv2.imread('source.jpg')

	if True:
		image = cv2.imread('bluethumbtacks.png')	
		#let user select region
		cv2.namedWindow('clickme4x')
		cv2.setMouseCallback('clickme4x', point_collection)
		cv2.imshow('clickme4x', image)
		print "passed imshow"
		cv2.waitKey(6000)
		print "passed waitkey"
		cv2.destroyAllWindows()
		print pts_src

	# with picamera.PiCamera() as camera:
	# 	# Set resolution of camera and the framerate
	# 	# A higher fps won't necessarily result in faster images
	#	 camera.resolution = (image_width, image_height)
	#	 camera.framerate = 30
	#	 camera.capture_sequence(streams(), use_video_port=True)


if __name__ == "__main__":
	main()