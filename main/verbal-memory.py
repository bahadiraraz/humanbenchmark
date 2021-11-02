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

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
flag2 = True
flag4 = False
mouse = Controller()
main_word_list = list()

time.sleep(1)
mouse.position = (950, 450)
mouse.click(Button.left, 1)


def get_number():
	global flag2, flag4
	while True:
		stc = mss.mss()
		scr = stc.grab(
			{
				"left": 790,
				"top": 280,
				"width": 300,
				"height": 80,
			}
		)
		frame = np.array(scr)
		try:
			print(pytesseract.image_to_string(frame).splitlines())
			if pytesseract.image_to_string(frame).splitlines()[0] not in main_word_list:
				main_word_list.append(pytesseract.image_to_string(frame).splitlines()[0])
				mouse.position = (250 + 744, 230 + 152)
				mouse.click(Button.left, 1)
				time.sleep(0.3)
			elif pytesseract.image_to_string(frame).splitlines()[0] in main_word_list:
				mouse.position = (180 + 744, 230 + 152)
				mouse.click(Button.left, 1)
				time.sleep(0.3)
		except IndexError:
			pass
		if flag2 == False:
			break


threading.Thread(target=get_number).start()

while True:
	stc = mss.mss()
	scr = stc.grab(
		{
			"left": 744,
			"top": 152,
			"width": 420,
			"height": 480,
		}
	)
	frame = np.array(scr)
	print(main_word_list)
	try:
		cv2.putText(frame, "word " + main_word_list[-1], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
		cv2.putText(frame, "word count " + str(len(main_word_list)), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
					2)
	except IndexError:
		pass
	cv2.imshow("main", frame)
	cv2.setWindowProperty("main", cv2.WND_PROP_TOPMOST, 1)

	if cv2.waitKey(1) & 0xFF == ord("q"):
		cv2.destroyAllWindows()
		cv2.waitKey(1)
		flag2 = False
		sys.exit()
