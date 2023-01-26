import numpy as np
from numpy import ndarray
import random


# 添加高斯噪声
def gauss_noise(img: ndarray, **args) -> ndarray:
    noise = np.random.normal(0, 0.05, img.shape).astype(dtype=np.float32) 
    img = img + noise
    img = np.clip(img, 0, 1)
    return np.uint8(img * 255)


# 添加椒盐噪声
def sp_noise(img: ndarray, **args) -> ndarray:
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if random.random() < 0.02:
                img[i][j] = 0 if random.random() < 0.5 else 1
    return np.uint8(img * 255)


# 实现中值滤波
def median_filter(img: ndarray, **args) -> ndarray:
    windows_size = 3
    edge = np.floor(windows_size/2).astype(dtype=np.int64) 
    h, w = img.shape[0], img.shape[1]
    new_img = np.array(img)
    for i in range(edge, h - edge):
        for j in range(edge, w - edge):
                windows_array = np.array(img[i - edge : i + edge + 1, 
                                            j - edge : j + edge + 1])
                #彩色图像的情况
                if (img[0,0].size == 3):
                    new_img[i, j] = np.median(np.median(windows_array, axis = 1), axis = 0)
                #黑白图像的情况
                else: 
                    new_img[i, j] = np.median(windows_array)  
    return np.uint8(new_img * 255)

# 实现均值滤波
def means_filter(img: ndarray, **args) -> ndarray:
    windows_size = 3
    edge = np.floor(windows_size/2).astype(dtype=np.int64) 
    h, w = img.shape[0], img.shape[1]
    new_img = np.array(img)
    for i in range(edge, h - edge):
        for j in range(edge, w - edge):
                windows_array = np.array(img[i - edge : i + edge + 1, 
                                            j - edge : j + edge + 1])
                #彩色图像的情况
                if (img[0,0].size == 3):
                    new_img[i, j] = np.mean(np.mean(windows_array, axis = 1), axis = 0)
                #黑白图像的情况
                else: 
                    new_img[i, j] = np.mean(windows_array)  
    return np.uint8(new_img * 255)


# 实现直方图均衡化
def equalize(img: ndarray, **args) -> ndarray:
    if (img[0,0].size == 3):
        img = np.array(img[:,:,0])
    h, w = img.shape[0], img.shape[1]
    hist = np.zeros(256)
    for i in range(h):
        for j in range(w):
            hist[(img[i,j]*255).astype(dtype=np.int64)] += 1
    hist = hist / (h * w)
    hp = np.zeros(256)
    for i in range(256):
        for j in range(i+1):
            hp[i] += hist[j]
    hp = np.clip(hp, 0, 1)
    for i in range(h):
        for j in range(w):
            img[i,j] = hp[(img[i,j]*255).astype(dtype=np.int64)]        
    return np.uint8(img * 255)


# 实现直方图归一化
def normalize(img: ndarray, **args) -> ndarray:
    if (img[0,0].size == 3):
        img = np.array(img[:,:,0])
    h, w = img.shape[0], img.shape[1]
    min_pexel = img.min()
    max_pexel = img.max()
    for i in range(h):
        for j in range(w):
            img[i,j] = (img[i,j] - min_pexel) / (max_pexel - min_pexel)
    img = np.clip(img, 0, 1)
    return np.uint8(img * 255)


# 实现膨胀运算
def dilate(img: ndarray, **args) -> ndarray:
    windows_size = 3
    edge = np.floor(windows_size/2).astype(dtype=np.int64) 
    h, w = img.shape[0], img.shape[1]
    new_img = np.array(img)
    for i in range(edge, h - edge):
        for j in range(edge, w - edge):
            windows_array = np.array(img[i - edge : i + edge + 1, 
                                        j - edge : j + edge + 1])
            #print (windows_array)
            new_img[i, j] = np.max(windows_array)  
            #print (np.max(windows_array))
    return np.uint8(new_img * 255)


# 实现腐蚀运算
def erode(img: ndarray, **args) -> ndarray:
    windows_size = 3
    edge = np.floor(windows_size/2).astype(dtype=np.int64) 
    h, w = img.shape[0], img.shape[1]
    new_img = np.array(img)
    for i in range(edge, h - edge):
        for j in range(edge, w - edge):
            windows_array = np.array(img[i - edge : i + edge + 1, 
                                        j - edge : j + edge + 1])
            new_img[i, j] = np.min(windows_array)  
    return np.uint8(new_img * 255)
