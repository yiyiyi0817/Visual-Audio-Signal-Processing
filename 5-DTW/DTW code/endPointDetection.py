import wave
import os
import numpy as np


def get_energy_array(wave_data, nframes):
    num = np.ceil(nframes / 256).astype(int)
    # 储存一帧（大多数256采样值）的能量的序列
    energy_array = np.zeros(num)
    for i in range(num):
        sum = 0
        for j in range(256 if i != num - 1 else (nframes - (num - 1) * 256)):
            sum += (int(wave_data[i * 256 + j]) ** 2)
        energy_array[i] = sum
    #print (energy_array)
    return energy_array 

def sgn(x):
    if x >= 0 :
        return 1
    else :
        return -1
    
def get_ZeroCrossingRate_array(wave_data, nframes):
    num = np.ceil(nframes / 256).astype(int)
    # 储存一帧（大多数256采样值）的过零率的序列
    zero_array = np.zeros(num)
    for i in range(num):
        sum = 0
        N = 256 if i != num - 1 else (nframes - (num - 1) * 256)
        for j in range(N):
            m = i * 256 + j
            if m == 0:
                pass
            else:
                sum += np.abs((sgn(wave_data[m]) - sgn(wave_data[m - 1])))
        zero_array[i] = float(sum)/(2 * N)
    #print (energy_array)
    return zero_array 


def ComputeThreshold(energy_array, ZeroCrossingRate_array):
    # volTh=(volMax-volMin)*epdPrm.volRatio+volMin; where epdPrm.volRatio is 0.03
    M_H = np.min(energy_array) + 0.001 * (np.max(energy_array) - np.min(energy_array))
    # 假定语音前10帧为静音段，静音段音量和过零率满足高斯分布
    # 则根据3σ原则，静音段能量 < μ + 3σ(即M_L)， 过零率 < μ + 3σ(即Z_s)
    en_mean = np.mean(energy_array[:10])
    en_sigma = np.std(energy_array[:10], ddof = 1)
    M_L = en_mean + 3 * en_sigma
    #M_L = (M_L + M_H) / 2
    zero_mean = np.mean(ZeroCrossingRate_array[:10])
    zero_sigma = np.std(ZeroCrossingRate_array[:10], ddof = 1)
    Z_s = zero_mean + 3 * zero_sigma
    #print (M_H, M_L, Z_s)
    return M_H, M_L, Z_s


# 根据双门限法返回各帧标签组成的列表（语音/静音）
def end_point_detection(energy_array, ZeroCrossingRate_array,  
                        M_H, M_L, Z_s, num):
    # label为0表示非语音帧，label为1表示语音帧，label为0表示静音帧
    label_lst = np.zeros(num, dtype = bool)
    # 存储根据M_H阈值得到的语音段端点对
    MH_endpoint = []
    # 根据M_H更改语音标签，并记录根据M_H得到的端点对
    for i in range(num):
        if energy_array[i] > M_H:
            label_lst[i] = 1
            if i == 0 or label_lst[i - 1] == 0:
                temp_start = i
            if i == num - 1:
                temp_end = i
                MH_endpoint.append([temp_start, temp_end])
        else:
            if i > 0 and label_lst[i - 1] == 1:
                temp_end = i - 1
                MH_endpoint.append(np.array([temp_start, temp_end]))
    #print (MH_endpoint)
           
    # 存储根据M_L阈值得到的语音段左端点列表
    ML_endpoint = []
    # 根据M_H得到的端点对分别向两端根据M_L搜索
    for i in range(len(MH_endpoint)):
        # 向左端点左侧根据M_L搜索
        pLeft = MH_endpoint[i][0]
        while True:
            # 搜到第一帧或与之前的语音段相连时，停止搜索，不记录端点
            if pLeft == 0 or label_lst[pLeft - 1] == 1:
                break
            # 搜到左一帧为语音帧时，改变标签，继续向搜索
            elif energy_array[pLeft - 1] > M_L:
                label_lst[pLeft - 1] = 1
                pLeft -= 1
            # 搜到左一帧为非语音帧时，记录端点，停止搜索
            else:
                ML_endpoint.append(pLeft)
                break
            
        # 向右端点右侧根据M_L搜索（但不记录根据M_L得到的端点）
        pRight = MH_endpoint[i][1]
        while True:
            if pRight == num - 1 or label_lst[pRight + 1] == 1:
                break
            elif energy_array[pRight + 1] > M_L:
                label_lst[pRight + 1] = 1
                pLeft += 1
            else:
                break
    #print (ML_endpoint)
    
    # 根据M_L得到的端点对向左侧根据过零率搜索
    for index in ML_endpoint:
        i = index
        while True:
            if i == 0 or label_lst[i - 1] == 1:
                break
            elif ZeroCrossingRate_array[i - 1] > Z_s:
                label_lst[i - 1] = 1
                i -= 1   
            else:
                break
    #print (label_lst)            
    return label_lst

def get_pcm(wave_data, label_lst, num, fileNumber, pcm_path):
    new_wave_data = []
    for i in range(num - 1):
        if label_lst[i] == 1:
            for j in range(256):
                new_wave_data.append(wave_data[i * 256 + j])
        if label_lst[num - 1] == 1:
            for k in range(len(wave_data) % 256):
                new_wave_data.append(wave_data[(num - 1) * 256 + k])
        
    new_wave_data = np.array(new_wave_data, dtype = np.short)
    filename = fileNumber + '.pcm'
    folder = os.path.exists(pcm_path)
    if not folder:                 
        os.makedirs(pcm_path)  
    new_wave_data.tofile(pcm_path + filename)
    print ('成功生成：' + filename)
    
def main(train_num, filepath, pcm_path):
    for i in range(train_num):
        filename = os.listdir(filepath)
        # 打开一个声音文件，返回一个声音的实例
        f = wave.open(filepath + '/' + filename[i], 'r')
        # 一次性返回所有的音频参数，返回的是一个元组
        params = f.getparams()
        # 声道数，量化位数(byte单位)，采样频率，采样点数
        # 量化位数为用多少bit表达一次采样所采集的数据，1byte=8bits
        #print (params)
        nchannels, sampwidth, framerate, nframes = params[:4]
        # readframes返回的是二进制数据（一大堆bytes)，在Python中用字符串表示二进制数据。
        str_data = f.readframes(nframes)
        # 转成二字节数组形式（每个采样点占两个字节，即short）
        wave_data = np.frombuffer(str_data, dtype = np.short)
        f.close()
        
        # 256个采样点为一帧，某文件总帧数为num
        num = np.ceil(nframes / 256).astype(int)
        energy_array = get_energy_array(wave_data, nframes)
        ZeroCrossingRate_array = get_ZeroCrossingRate_array(wave_data, nframes)
        
        M_H, M_L, Z_s = ComputeThreshold(energy_array, ZeroCrossingRate_array)
        frames_lable = end_point_detection(energy_array, ZeroCrossingRate_array,
                                           M_H, M_L, Z_s, num)
        get_pcm(wave_data, frames_lable, num, filename[i][:-4], pcm_path)
        
        
