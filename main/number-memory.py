import shlex
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

white_box_cordinates = set()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
flag = ""
flag2 = True
flag3 = set()
mouse = Controller()

time.sleep(1)
mouse.position = (950,444)
mouse.click(Button.left, 1)

def get_number():
	global flag, flag2, flag3, flag4
	while True:
		stc = mss.mss()
		scr = stc.grab(
			{
				"left": 563,
				"top": 260,
				"width": 777,
				"height": 100,
			}
		)
		frame = np.array(scr)
		#using morphology to remove noise from the image and convert it to black and white
		hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		thresh = cv2.threshold(hsvframe, 220, 255, cv2.THRESH_BINARY)[1]
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
		close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
		# kernal = np.ones((5, 5), "uint8")
		# white_mask = cv2.dilate(white_mask, kernal)
		result = 255 - close
		a = pytesseract.image_to_boxes(result, config='--oem 3 --psm 6 outputbase digits')
		flag = "".join([x.split()[0] for x in a.splitlines() if x.split()[0].isdigit()])

		if flag2 == False or keyboard.is_pressed("q"):
			break

#using threding because so that it doesn't block opencv loop
threading.Thread(target=get_number).start()


# 259
def clicker():
	points = list(white_box_cordinates)
	for i in points:
		mouse = Controller()
		mouse.position = (i[0] + 744, i[1] + 130)
		mouse.click(Button.left, 1)



while True:
	stc = mss.mss()
	# Get raw pixels from the screen, save it to a Numpy array
	scr = stc.grab(
		{
			"left": 563,
			"top": 260,
			"width": 777,
			"height": 100,
		}
	)
	frame = np.array(scr)
	#white mask for the frame
	hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_white = np.array([0, 0, 0], dtype=np.uint8)
	upper_white = np.array([0, 0, 255], dtype=np.uint8)
	white_mask = cv2.inRange(hsvframe, lower_white, upper_white)
	#according to color density and when color density is greater than we enter numbers
	if round(np.average(hsvframe[50:, :, 0])) == 105:

		keyboard.write(flag,delay=0.2)
		time.sleep(1)
		mouse.position = (955, 400)
		mouse.click(Button.left, 1)
		time.sleep(1)
		mouse.position = (955, 444)
		mouse.click(Button.left, 1)
	# kernal = np.ones((4, 4), "uint8")
	# white_mask = cv2.dilate(white_mask, kernal)
	#put number in frame
	cv2.putText(frame, f"number: {flag}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), )
	#show the frame
	cv2.imshow("main", frame)
	cv2.setWindowProperty("main", cv2.WND_PROP_TOPMOST, 1)
	#if we press q then it will break
	if cv2.waitKey(1) & 0xFF == ord("q"):
		cv2.destroyAllWindows()
		cv2.waitKey(1)
		flag2 = False
		sys.exit()
