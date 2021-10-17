import sys
from cv2 import cv2
import numpy as np
import mss
from itertools import islice
from pynput.mouse import Button, Controller

mouse = Controller()
#opencv main loop
while True:
	stc = mss.mss()
	# Get raw pixels from the screen, save it to a Numpy array
	scr = stc.grab(
		{
			"left": 540,
			"top": 152,
			"width": 800,
			"height": 390,
		}
	)
	#detecting the circle and the center of the circle
	frame = np.array(scr)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=30, maxRadius=50)
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
		for (x, y, r) in circles:
			cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			#click the center point of the circle
			mouse.position = (x+540, y+152)
			mouse.click(Button.left, 1)
	#show the frame
	cv2.imshow("main", frame)
	cv2.setWindowProperty("main", cv2.WND_PROP_TOPMOST, 1)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		cv2.destroyAllWindows()
		cv2.waitKey(1)
		flag2 = False
		sys.exit()
