
import cv2, time 
import numpy

first_frame = None
video = cv2.VideoCapture(0)

#frm counts what frame we are on 
frm = 0 

#pause is used to avoid taking an exessive
#amount of photos 
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

	#After the start frame is grabbed, we start detecting
	#motion. 
	if frm > 5: 
		delta_frame = cv2.absdiff(first_frame, gray)
		thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
		thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)

		cnts,a = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for contour in cnts:

			if cv2.contourArea(contour) < 1000:
				continue

			if pause > 20:
				(x, y, w, h) = cv2.boundingRect(contour)
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
				print("[-] ALERT: Motion detected!")
				timestamp = str(time.time())
				cv2.imwrite("images/frame{}.jpg".format(timestamp), frame)
				#Reset the "timer". 10 frames later we recapture motion
				#if there is any. 
				pause = 0


		cv2.imshow("capturing", frame)

		key = cv2.waitKey(1)

		#Press x to quit
		if key == ord('x'):
			break 


video.release()

cv2.destroyAllWindows()