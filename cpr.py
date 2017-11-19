#import gopigo
#import picamera
import cv2
import time
import cStringIO
import numpy as np

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
	homography(image)
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


def main():
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
		homography(image)

	# with picamera.PiCamera() as camera:
	# 	# Set resolution of camera and the framerate
	# 	# A higher fps won't necessarily result in faster images
	#	 camera.resolution = (image_width, image_height)
	#	 camera.framerate = 30
	#	 camera.capture_sequence(streams(), use_video_port=True)


if __name__ == "__main__":
	main()