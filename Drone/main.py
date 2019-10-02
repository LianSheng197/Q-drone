import numpy as np
import cv2
import camera
import arduino
import time


Drone_start=False
arduino_str=""
Height=0.0

#pitch_PID
pitch_range=200
pitch_MID=1490
pitch_MAX=pitch_MID+pitch_range
pitch_MIN=pitch_MID-pitch_range
pitch_Kp=0.7
pitch_Ki=0.0001
pitch_Kd=0.01
pitch_sum=0.0
pitch_olderror=0.0

def pitch_PID(error):
    global pitch_sum,pitch_olderror,pitch_Kp,pitch_Ki,pitch_Kd,pitch_MAX,pitch_MIN,pitch_MID
    pitch_sum+=error
    last_error =error-pitch_olderror
    pitch_olderror=error
    pitch_out=error*pitch_Kp+pitch_sum*pitch_Ki+last_error*pitch_Kd+pitch_MID
    if(pitch_out>pitch_MAX):
        pitch_out=pitch_MAX
    elif(pitch_out<pitch_MIN):
        pitch_out=pitch_MIN
    return pitch_out

#roll_PID
roll_range=200
roll_MID=1490
roll_MAX=roll_MID+roll_range
roll_MIN=roll_MID-roll_range
roll_Kp=0.5
roll_Ki=0.0001
roll_Kd=0.01
roll_sum=0.0
roll_olderror=0.0 

def roll_PID(error):
    global roll_sum,roll_olderror,roll_Kp,roll_Ki,roll_Kd,roll_MAX,roll_MIN,roll_MID
    roll_sum+=error
    last_error=error-roll_olderror
    roll_olderror=error
    roll_out=error*roll_Kp+roll_sum*roll_Ki+last_error*roll_Kd+roll_MID
    if(roll_out>roll_MAX):
        roll_out=roll_MAX
    elif(roll_out<roll_MIN):
        roll_out=roll_MIN
    return roll_out


#zeroing_PID_value
def zeroing():
    global roll_sum,roll_olderror,pitch_sum,pitch_olderror
    roll_sum=0.0
    pitch_sum=0.0
    roll_olderror=0.0
    pitch_olderror=0.0


# Init
print("[INFO] init_\n")
sum_dir=np.zeros(2)
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

while(True):
    try:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        LK=camera.LK(frame,200)
        break
    except:
        continue

print("[INFO] while: cap is opening\n")
while cap.isOpened():
    arduino_str=arduino.Arduino.isOpen()
    arduino_str=arduino_str[:-2]

    if(arduino_str== "<OPEN>"):
        print("OPEN")
        Drone_start=True
    elif(arduino_str == "<CLOSE>"):
        Drone_start=False
    elif(arduino_str != ""):
        Height=float(arduino_str)
            
    if(Drone_start):
        try:
            ret, frame = cap.read()
            if(cap.get(5)==-1):
                count_dir[0]=1490
                count_dir[1]=1490
                count_dir[2]=0
                count_dir[3]=1490
                break
                print("Error1")
            elif(frame is not None):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                list_dir=LK.speed(frame)
                for i in range(2):
                    tmp=float(list_dir[i]*Height/100)
                    if(tmp<-40.0):
                        tmp=-40.0
                    elif(tmp>40.0):
                        tmp=40.0
                    sum_dir[i]+=tmp
                    count_dir[i]=int(sum_dir[i])
                if(Height>30):
                    count_dir[0]=roll_PID(count_dir[0])
                    count_dir[1]=pitch_PID(count_dir[1])
                else:
                    count_dir[0]=1490
                    count_dir[1]=1490
                    sum_dir[0]=0
                    sum_dir[1]=0
                    zeroing()
                count_dir[2]=1
                count_dir[3]=1490
                print(count_dir," ",Height)

            else:
                count_dir[0]=1490
                count_dir[1]=1490
                count_dir[2]=0
                count_dir[3]=1490
                print("Error2")
                break
        except:
            count_dir[0]=1490
            count_dir[1]=1490
            count_dir[2]=0
            count_dir[3]=1490
            break

    else:
        count_dir[0]=1490
        count_dir[1]=1490
        count_dir[2]=0
        count_dir[3]=1490
        sum_dir[0]=0
        sum_dir[1]=0
        zeroing()

    Arduino.send(count_dir)
    
print("End")		
        

cap.release()
cv2.destroyAllWindows()
            
    

count_dir[4]=1

