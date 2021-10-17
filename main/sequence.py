import sys
import time
from cv2 import cv2
import numpy as np
import mss
from itertools import islice
from pynput.mouse import Button, Controller
import pytesseract
import threading
import keyboard

white_box_cordinates = list()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
flag = 1
flag2 = True
flag4 = False
mouse = Controller()
mouse.position = (950, 432)
mouse.click(Button.left, 1)
time.sleep(0.5)
first_time = time.time()
number = 1
ggg = 0.22


def get_number():
	global flag, flag2, number
	while True:
		try:
			stc = mss.mss()
			scr = stc.grab(
				{
					"left": 744,
					"top": 130,
					"width": 400,
					"height": 400,
				}
			)
			frame = np.array(scr)
			hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			thresh = cv2.threshold(hsvframe, 220, 255, cv2.THRESH_BINARY)[1]
			kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
			close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
			# kernal = np.ones((5, 5), "uint8")
			# white_mask = cv2.dilate(white_mask, kernal)
			result = 255 - close

			a = pytesseract.image_to_boxes(result, config='--oem 3 --psm 6 outputbase digits')
			print(a)
			gg = "".join([x.split()[0] for x in a.splitlines() if int(x.split()[2]) > 160 and x.split()[0].isdigit()])
			flag = gg
			if flag2 == False:
				break
		except Exception:
			pass


# threading.Thread(target=get_number).start()

def clicker():
	points = list(white_box_cordinates)
	for i in points:
		mouse.position = (i[0] + 744, i[1] + 130)
		mouse.click(Button.left, 1)
		time.sleep(0.3)


while True:
	stc = mss.mss()
	scr = stc.grab(
		{
			"left": 744,
			"top": 130,
			"width": 400,
			"height": 400,
		}
	)
	frame = np.array(scr)
	hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_white = np.array([0, 0, 0], dtype=np.uint8)
	upper_white = np.array([0, 0, 255], dtype=np.uint8)
	white_mask = cv2.inRange(hsvframe, lower_white, upper_white)

	# kernal = np.ones((5, 5), "uint8")
	# white_mask = cv2.dilate(white_mask, kernal)
	res_white = cv2.bitwise_and(frame, frame, mask=white_mask)
	countours = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
	countours = sorted(countours, key=cv2.contourArea, reverse=True)[:200]
	a = pytesseract.image_to_boxes(frame[:, :, 2], config='--oem 3 --psm 6 outputbase digits')
	print(a)
	gg = "".join([x.split()[0] for x in a.splitlines() if int(x.split()[2]) > 160 and x.split()[0].isdigit()])
	flag = gg

	for contour in countours:
		area = cv2.contourArea(contour)
		if area > 150:
			x1, y1, w1, h1 = cv2.boundingRect(contour)
			x_white = int(x1 + w1 / 2)
			y_white = int(y1 + h1 / 2)
			if y_white > 50:
				frame_red_bar = cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
				cv2.putText(frame, "white box", (x1 + w1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), )
				cv2.circle(frame, (x_white, y_white), 3, (0, 255, 0), -1)
				cv2.putText(frame, f"{x_white, y_white}", (x_white, y_white), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
							(0, 255, 0), )


			def get_second_element(a):
				return list(islice(a, 1, None))[0]


			def get_all_second_element(a):
				b = []
				for i in a:
					b.append(get_second_element(i))
				return b


			try:
				if y_white > 50 and len(white_box_cordinates) < int(flag):
					if white_box_cordinates == list():
						white_box_cordinates.append((x_white, y_white))
					elif white_box_cordinates[-1] != (x_white, y_white):
						white_box_cordinates.append((x_white, y_white))
			except Exception:
				pass
	try:
		print("--------")
		print(flag, white_box_cordinates)
		print(time.time() - first_time)
		print(1 + ggg)
		print("--------")

		if len(white_box_cordinates) == int(flag) and time.time() - first_time > 0.85 + ggg:
			clicker()
			ggg += 0.9
			first_time = time.time()
			white_box_cordinates.clear()
	except ValueError:
		pass
	cv2.putText(frame, f"level: {flag}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), )
	cv2.imshow("main", frame)
	cv2.setWindowProperty("main", cv2.WND_PROP_TOPMOST, 1)

	if cv2.waitKey(1) & 0xFF == ord("q"):
		cv2.destroyAllWindows()
		cv2.waitKey(1)
		flag2 = False
		sys.exit()
