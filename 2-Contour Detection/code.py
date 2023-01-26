import cv2
import numpy as np
from sklearn.cluster import KMeans


#打开原图img_color和灰度图像img
img_color = cv2.imread('test1.png',1)
img = cv2.imread('test1.png',0)
cv2.imshow('image',img)

#OSTU二值化，th1返回阈值，ret1返回二值化的结果图像
th1, ret1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)


#因为轮廓检测是在黑底图上检测白色边缘，对之前的图像进行反相（之前的图像是白底黑色物体）
dst = cv2.bitwise_not(ret1)

kernel=np.ones((5,5),np.uint8)#构造5x5卷积核
dilation=cv2.dilate(dst,kernel,iterations=5) #进行5次膨胀
erosion=cv2.erode(dilation,kernel,iterations=5)#进行5次腐蚀

#轮廓检测：cv2.RETR_EXTERNAL只检测最外围轮廓，包含在外围轮廓内的内围轮廓被忽略
contours,hierarchy=cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#遍历得到每个轮廓的面积，存储进area_lst数组
area_lst = np.array([])
for cnt in contours:
    tempS=cv2.contourArea(cnt)
    area_lst = np.append(area_lst, tempS)
print (area_lst)

#用K-means算法将面积数据分成两个簇，面积大的代表橘子簇，面积小的代表枣子簇
y = area_lst.reshape(-1,1)
km = KMeans(2)
km.fit(y)
if ( km.cluster_centers_[0] < km.cluster_centers_[1]):
    orange_lable = 1
else:
    orange_lable = 0
print ('枣子的数量是：',np.sum(km.labels_ == 1 - orange_lable))
print ('橘子的数量是：',np.sum(km.labels_ == orange_lable))

#在img中画出得到的轮廓边缘
cv2.drawContours(img_color,contours,-1,(0, 0, 255),3)

cv2.imshow('image',img_color)
cv2.waitKey(0)
cv2.destroyAllWindows()