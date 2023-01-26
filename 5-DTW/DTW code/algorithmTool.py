import struct
import numpy as np
import sys


def read_mfc(filename):
    f = open(filename, 'rb')
    '''
    nframes: number of frames 采样点数
    frate: frame rate in 100 nano-seconds unit
    nbytes: number of bytes per feature value
    feakind: 9 is USER
    '''
    nframes,frate,nbytes,feakind = struct.unpack('>IIHH', f.read(12))
    ndim = nbytes // 4  # feature dimension(4 bytes per value) 39维度
    
    mfcc = np.zeros((nframes, ndim))
    for i in range(nframes):
        for j in range(ndim):
            mf = f.read(4)
            c = struct.unpack('>f', mf)
            mfcc[i, j] = c[0]
    f.close()
    return mfcc


def dtw(mfc_data1, mfc_data2):
    len1 = mfc_data1.shape[0]
    len2 = mfc_data2.shape[0]
    # 记录代价矩阵
    Cost = np.zeros((len1 + 1, len2 + 1))
    # 记录路径
    Path = np.zeros((len1 + 1, len2 + 1,2)) 

    # 左下增加一圈无穷大的数，达到限制边界的目的
    for i in range(1, len1 + 1):
        Cost[i][0] = sys.maxsize
    for j in range(1, len2 + 1):
        Cost[0][j] = sys.maxsize

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            # 两39维向量的欧氏距离
            d = np.linalg.norm(mfc_data1[i-1] - mfc_data2[j-1])  
            a1 = 2 * d + Cost[i-1, j-1] if (i != 1 or j != 1) else d
            a2 = d + Cost[i-1, j]
            a3 = d + Cost[i, j-1]
            minFai = min(a1, a2, a3)
            Cost[i, j] = minFai
            if minFai == a1:
                Path[i, j] = [i-1, j-1]
            elif minFai == a2:
                Path[i, j] = [i-1, j]
            else:
                Path[i, j] = [i, j-1]
    # 返回归一化最终Cost
    return Cost[len1][len2]/(len1 + len2 - 2), Path


# 和dtw函数返回的Path配合使用
def get_same_len(mfc_array, Path):
    len1 = Path.shape[0] - 1
    len2 = Path.shape[1] - 1
    new_array = np.zeros((len1, mfc_array.shape[1]))
    Path[0, 0] = np.array([-1, -1])
    
    m = np.array([len1, len2])
    for i in range(len1 - 1, -1, -1):
        count = 0
        sum_array = np.zeros(mfc_array.shape[1])
        while True:
            sum_array = sum_array + mfc_array[int(m[1]-1)]
            count += 1 
            pm = Path[int(m[0]), int(m[1])]
            if pm[1] != i:
                    break  
            m = pm
        new_array[i] = sum_array / count
        m = pm
    return new_array
