import numpy as np
import cv2
import time
class LK():
    def __init__(self,image):
        self.feature_params = dict(maxCorners=10,qualityLevel=0.3,minDistance=20,blockSize=40)
        self.lk_params = dict(winSize=(15,15),maxLevel=2,criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,0.03))
        self.old_gray = image
        '''High=100
	Width=300
	image_high  = int(np.shape(new_frame)[0]/2)
	image_width = int(np.shape(new_frame)[1]/2)
	frame = new_frame[ image_high-High : image_high+High,image_width-Width:image_width+Width ]'''
        self.p0 = cv2.goodFeaturesToTrack(image, mask = None, **self.feature_params)
        self.start_time=time.time()
    
    def speed(self,frame_gray):
        record_time=time.time()
        err_time=record_time-self.start_time
        self.start_time=record_time
        p1,st,err = cv2.calcOpticalFlowPyrLK(self.old_gray,frame_gray,self.p0,None,**self.lk_params)
        good_new=p1[st==1]
        good_old=self.p0[st==1]
        count=0
        dir_Val=np.zeros(2)

        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            count+=1
            dir_Val[0]+=c-a
            dir_Val[1]+=b-d
        dir_Val/=count
        # cv2.imshow('My Image', frame_gray)

        cv2.waitKey(5)

       	self.old_gray = frame_gray.copy()
        self.p0 = cv2.goodFeaturesToTrack(self.old_gray, mask = None, **self.feature_params)
        return dir_Val

