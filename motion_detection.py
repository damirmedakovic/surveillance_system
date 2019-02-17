
import cv2, time 
import numpy

first_frame = None
video = cv2.VideoCapture(0)

frm = 0 
pause = 0

while True:

	frm = frm + 1
	pause = pause + 1

	check, frame = video.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)


	#Grab 5th frame as reference frame so that the
	#camera has time to adjust.
	if first_frame is None and frm == 5:
		first_frame = gray
		cv2.imshow("first", first_frame)
		continue

	if frm > 5: 
		delta_frame = cv2.absdiff(first_frame, gray)
		thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
		thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)

		cnts,a = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for contour in cnts: 
			if cv2.contourArea(contour) < 1000:
				continue
			if pause > 10:
				(x, y, w, h) = cv2.boundingRect(contour)
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
				print("ALERT")
				cv2.imwrite("images/frame{}.jpg".format(frm), frame)
				pause = 0


		cv2.imshow("capturing", frame)
		cv2.imshow("gray", gray)

		key = cv2.waitKey(1)

		if key == ord('q'):
			break 


video.release()

cv2.destroyAllWindows()