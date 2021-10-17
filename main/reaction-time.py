import sys
from cv2 import cv2
import numpy as np
import mss
from pynput.mouse import Button, Controller

while True:
	stc = mss.mss()
	scr = stc.grab(
		{
			"left": 744,
			"top": 152,
			"width": 420,
			"height": 240,
		}
	)
	frame = np.array(scr)
	hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_white = np.array([36, 25, 25], dtype=np.uint8)
	upper_white = np.array([86, 255, 255], dtype=np.uint8)
	white_mask = cv2.inRange(hsvframe, lower_white, upper_white)

	res_white = cv2.bitwise_and(frame, frame, mask=white_mask)
	countours = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
	# more sensitive contours
	countours = sorted(countours, key=cv2.contourArea, reverse=True)[:100]

	for contour in countours:
		area = cv2.contourArea(contour)
		if area > 150:
			x1, y1, w1, h1 = cv2.boundingRect(contour)
			x_green = int(x1 + w1 / 2)
			y_green = int(y1 + h1 / 2)
			if y_green > 50:
				# click green
				mouse = Controller()
				mouse.position = (800, 200)
				mouse.click(Button.left, 1)

	cv2.imshow("main", frame)
	cv2.setWindowProperty("main", cv2.WND_PROP_TOPMOST, 1)

	if cv2.waitKey(1) & 0xFF == ord("q"):
		cv2.destroyAllWindows()
		cv2.waitKey(1)
		flag2 = False
		sys.exit()
