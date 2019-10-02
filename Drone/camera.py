import numpy as np
import cv2
import time
import math
class LK():
    def __init__(self,image,Filter):
        self.filter_range=Filter
        self.feature_params = dict(maxCorners=10 ,qualityLevel=0.6,minDistance=7,blockSize=7)
        self.lk_params = dict(winSize=(15,15),maxLevel=2,criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,0.03))
        self.old_gray =image.copy()
        ToTrack = image[240-int(self.filter_range/2):240+int(self.filter_range/2),320-int(self.filter_range/2):320+int(self.filter_range/2)]
        self.p0 = cv2.goodFeaturesToTrack(ToTrack, mask = None, **self.feature_params)

        for  i in range(self.p0.shape[0]):
            self.p0[i][0][0] = self.p0[i][0][0] + 320-int(self.filter_range/2)
            self.p0[i][0][1] = self.p0[i][0][1] + 240-int(self.filter_range/2)
        
        self.start_time=time.time()
    
    def speed(self,frame_gray):
        '''record_time=time.time()
        err_time=record_time-self.start_time
        self.start_time=record_time'''
        dir_Val=np.zeros(2)
        color = np.random.randint(0,255,(100,3))

        p1,st,err = cv2.calcOpticalFlowPyrLK(self.old_gray,frame_gray,self.p0,None,**self.lk_params)
        good_new=p1[st==1]
        good_old=self.p0[st==1]
        count=0
        
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            count+=1
            dir_Val[0]+=a-c
            dir_Val[1]+=d-b
 
        if count==0:
            dir_Val[0]=0
            dir_Val[1]=0
            return dir_Val
        else:
            if math.isnan(dir_Val[0]):
                dir_Val[0]=0
                dir_Val[1]=0
                return dir_Val
            elif math.isnan(dir_Val[1]):
                dir_Val[0]=0
                dir_Val[1]=0
                return dir_Val
            else:
                dir_Val/=count
        
        ToTrack = frame_gray[240-int(self.filter_range/2):240+int(self.filter_range/2),320-int(self.filter_range/2):320+int(self.filter_range/2)]
        point = cv2.goodFeaturesToTrack(ToTrack, mask = None, **self.feature_params)
        if point is not None:
            self.old_gray =frame_gray.copy()
            self.p0 = cv2.goodFeaturesToTrack(ToTrack, mask = None, **self.feature_params)
            for i in range(self.p0.shape[0]):
                self.p0[i][0][0] = self.p0[i][0][0] + 320-int(self.filter_range/2)
                self.p0[i][0][1] = self.p0[i][0][1] + 240-int(self.filter_range/2)

        
            
        return dir_Val

