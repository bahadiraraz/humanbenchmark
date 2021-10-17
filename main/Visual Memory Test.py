import sys
from cv2 import cv2
import numpy as np
import mss
from itertools import islice
from pynput.mouse import Button, Controller
import pytesseract
import threading
import keyboard
import time

white_box_cordinates = set()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
flag = 1
flag2 = True
mouse = Controller()
time.sleep(1)
mouse.position = (950,444)
mouse.click(Button.left, 1)

def get_number():
	global flag, flag2
	while True:
		stc = mss.mss()
		# Get raw pixels from the screen, save it to a Numpy array
		scr = stc.grab(
			{
				"left": 744,
				"top": 130,
				"width": 400,
				"height": 400,
			}
		)
		frame = np.array(scr)
		try:
			#detect number in the frame
			a = pytesseract.image_to_boxes(frame, config="digits").splitlines()
			print(a)
			gg = "".join([x.split()[0] for x in a if int(x.split()[1]) < 200 and x.split()[0].isdigit()])
			print(gg, white_box_cordinates)
			if gg == "0":
				clicker()
			if str(flag) == gg:
				clicker()
			else:
				flag = gg
				try:
					white_box_cordinates.clear()
				except TypeError:
					pass
			if flag2 == False or keyboard.is_pressed("q"):
				break
		except IndexError:
			pass

#using threding because so that it doesn't block opencv loop
threading.Thread(target=get_number).start()



def clicker():
	#click the white box in the white_box_cordinates
	points = list(white_box_cordinates)
	for i in points:
		mouse.position = (i[0] + 744, i[1] + 130)
		mouse.click(Button.left, 1)

#opencv main loop
while True:
	#press w to start recording
	stc = mss.mss()
	# Get raw pixels from the screen, save it to a Numpy array
	scr = stc.grab(
		{
			"left": 744,
			"top": 130,
			"width": 400,
			"height": 400,
		}
	)
	frame = np.array(scr)
	print(frame)
	#white mask for the frame
	hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_white = np.array([0, 0, 0], dtype=np.uint8)
	upper_white = np.array([0, 0, 255], dtype=np.uint8)
	white_mask = cv2.inRange(hsvframe, lower_white, upper_white)
	# kernal = np.ones((4, 4), "uint8")
	# white_mask = cv2.dilate(white_mask, kernal)
	res_white = cv2.bitwise_and(frame, frame, mask=white_mask)
	#detecting approximations of white boxes in the frame
	countours = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
	# more sensitive contours
	countours = sorted(countours, key=cv2.contourArea, reverse=True)[:200]
	#loop through the contours and draw the rectangles around the white boxes
	for contour in countours:
		area = cv2.contourArea(contour)
		if area > 150:
			x1, y1, w1, h1 = cv2.boundingRect(contour)
			x_white = int(x1 + w1 / 2)
			y_white = int(y1 + h1 / 2)
			if y_white > 50:
				cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
				cv2.putText(frame, "white box", (x1 + w1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0),2 )
				cv2.circle(frame, (x_white, y_white), 3, (0, 255, 0), -1)
				cv2.putText(frame, f"{x_white, y_white}", (x_white, y_white), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0),2 )

			
			def get_second_element(a):
				return list(islice(a, 1, None))[0]


			def get_all_second_element(a):
				b = []
				for i in a:
					b.append(get_second_element(i))
				return b

			#compare the white box cordinates
			if y_white + 1 not in get_all_second_element(white_box_cordinates) and y_white > 50:
				white_box_cordinates.add((x_white, y_white))

	#show the frame
	cv2.putText(frame, f"level: {flag}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), )
	cv2.imshow("main", frame)
	cv2.setWindowProperty("main", cv2.WND_PROP_TOPMOST, 1)
	#if pressed q then break
	if cv2.waitKey(1) & 0xFF == ord("q"):
		cv2.destroyAllWindows()
		cv2.waitKey(1)
		flag2 = False
		sys.exit()
