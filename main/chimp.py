import sys
import time
from cv2 import cv2
import numpy as np
import mss
from itertools import islice
from pynput.mouse import Button, Controller
import pytesseract
import threading

number_cordinates = list()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
flag = 1
flag2 = True
flag3 = set()
mouse = Controller()
stc = mss.mss()
numbers = ""
tt2 = ""


def get_number():
	global flag, flag2, flag3, stc, numbers, tt2
	while True:
		scr = stc.grab(
			{
				"left": 545,
				"top": 150,
				"width": 814,
				"height": 352,
			}
		)
		frame = np.array(scr)
		thresh = cv2.threshold(frame, 220, 255, cv2.THRESH_BINARY)[1]
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
		close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
		result = 255 - close
		numbers = pytesseract.image_to_boxes(result[:, :, 2], config='--oem 3 --psm 6 outputbase digits')
		# get string from image
		tt2 = pytesseract.image_to_string(frame).splitlines()[0]
		if flag2 == False:
			break


threading.Thread(target=get_number).start()


def clicker():
	points = number_cordinates
	for i in points:
		mouse.position = (i[1] + 545, i[2] + 150)
		mouse.click(Button.left, 1)
		time.sleep(0.25)


while True:
	stc = mss.mss()
	scr = stc.grab(
		{
			"left": 545,
			"top": 150,
			"width": 814,
			"height": 352,
		}
	)

	frame = np.array(scr)
	hx, hw = frame.shape[0], frame.shape[1]
	hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_white = np.array([64, 147, 213])
	upper_white = np.array([104, 178, 214])
	white_mask = cv2.inRange(hsvframe, lower_white, upper_white)
	kernal = np.ones((3, 3), "uint8")
	white_mask = cv2.dilate(white_mask, kernal)
	res_white = cv2.bitwise_and(frame, frame, mask=white_mask)

	countours = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
	countours = sorted(countours, key=cv2.contourArea, reverse=True)[:200]

	np_frame = np.array(frame)
	np_frame = np_frame[100:300, :, :]
	np_frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2HSV)
	lower_yellow = np.array([20, 100, 100])
	upper_yellow = np.array([30, 255, 255])
	yellow_mask = cv2.inRange(np_frame, lower_yellow, upper_yellow)

	for i in numbers.splitlines():
		i = i.split()
		try:
			number, x, y, w, h = int(i[0]), int(i[1]), int(i[2]), int(i[3]), int(i[4])
			if abs(w - h) > 20 and abs(w - h) < 5600 and not (cv2.countNonZero(yellow_mask) > 0) and \
					numbers.splitlines()[0][0] != "0":
				cv2.rectangle(frame, (x, hx - y), (w, hx - h), (0, 255, 0), 2)
				x_number = int(x + (w - x) / 2)
				y_number = int(hx - y - (h - y) / 2)
				cv2.putText(frame, str(number), (x, hx - y + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
				cv2.circle(frame, (x_number, y_number), 5, (0, 0, 255), -1)

				if (number, x_number, y_number) not in number_cordinates and not (cv2.countNonZero(yellow_mask) > 0):
					# short list by number value
					number_cordinates.append((number, x_number, y_number))
					number_cordinates = sorted(number_cordinates, key=lambda x: x[0])

		except ValueError:
			pass
	for contour in countours:
		area = cv2.contourArea(contour)
		if area > 600:
			x1, y1, w1, h1 = cv2.boundingRect(contour)
			if w1 > 60 and h1 > 60:
				x_white = int(x1 + w1 / 2)
				y_white = int(y1 + h1 / 2)

				cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
				cv2.putText(frame, "white box", (x1 + w1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), )
				cv2.circle(frame, (x_white, y_white), 3, (0, 255, 0), -1)
				cv2.putText(frame, f"{x_white, y_white}", (x_white, y_white), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
							(0, 255, 0), )

	if cv2.countNonZero(yellow_mask) > 0:
		print("yellow")
		mouse.position = (947, 437)
		mouse.click(Button.left, 1)
		flag += 1
		number_cordinates.clear()
	else:
		clicker()
		print(number_cordinates)
		print("no yellow")
	cv2.putText(frame, f"{flag}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), )
	cv2.imshow("main", frame)
	cv2.setWindowProperty("main", cv2.WND_PROP_TOPMOST, 1)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		cv2.destroyAllWindows()
		cv2.waitKey(1)
		flag2 = False
		sys.exit()
