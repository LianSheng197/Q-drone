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
ret, new_frame = cap.read()
High=100
Width=300
image_high  = int(np.shape(new_frame)[0]/2)
image_width = int(np.shape(new_frame)[1]/2)
frame = new_frame[ image_high-High : image_high+High,image_width-Width:image_width+Width ]
frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
LK=camera.LK(frame)

print("[INFO] while: cap is opening\n")
while cap.isOpened():
	ret, frame = cap.read()
	if(ret):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		list_dir=LK.speed(frame)
		'''for i in range(2):
			count_dir[i]=list_dir[i]'''
		for i in range(40):
			try:
				count_dir[0]=20*i+1100
				count_dir[1]=20*i+1100
				count_dir[2]=20*i+1100
				count_dir[3]=20*i+1100
				print(count_dir)
				Arduino.send(count_dir)
			except IOError:
				raise IOError()
				break	

count_dir[4]=1
Arduino.send(count_dir)
