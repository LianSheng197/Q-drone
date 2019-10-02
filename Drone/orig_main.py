import numpy as np
import cv2
import camera
import arduino

# Init
print("[INFO] init_\n")
count_dir=np.zeros((5), dtype=np.int)



Arduino=arduino.Arduino()
cap_count=0
while True:
	cap = cv2.VideoCapture(cap_count)
	if(cap.isOpened()):
		break
	elif(cap_count==8):
		cap_count=0
	else:
		cap_count+=1
print("[INFO] camera_open\n")
print(count_dir)
count_dir[4]=0
Arduino.send(count_dir)
ret, frame = cap.read()
print(frame.shape)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
LK=camera.LK(frame,300)

print("[INFO] while: cap is opening\n")
while cap.isOpened():
	ret, frame = cap.read()
	if(ret):

		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		list_dir=LK.speed(frame)
		for i in range(2):
			count_dir[i]=int(list_dir[i])

		print(count_dir)

			
	

		
count_dir[4]=1
Arduino.send(count_dir)
