import wave
import os
import numpy as np
import matplotlib.pyplot as plt


# a为正数
def Q_8bit(x, a):
    if x > 127 * a:
        return 127
    elif x < -128 * a:
        return -128
    else:
        return round(x/a)


def compress_to_8bit(wave_data, a):
    # 第一个采样值占16bits
    new_data = np.zeros(len(wave_data) + 1, dtype=np.int8)
    # 把第一个采样值按二进制的前8位和后8位分别存储在new_data[-1]和new_data[0]中
    new_data[-1] = np.int8((wave_data[0] + 32768) // 256 - 128)
    new_data[0] = np.int8((wave_data[0] + 32768) % 256 - 128)
    x_ = int(wave_data[0])
    for i in range(1, len(wave_data)):
        d = int(wave_data[i]) - int(x_)
        new_data[i] = Q_8bit(d, a)
        x_ += new_data[i] * a
    return new_data    


# a为正数, 要返回正数
def Q_4bit(x, a):
    if x > 7 * a:
        return 15
    elif x < -8 * a:
        return 0
    else:
        return round(x/a) + 8


# c为正数, 要返回正数
def Q_e(x, c):
    if x >= 0:
        return round(np.clip(-8 * np.exp(-c * x) + 7.5, -0.5+1e-8, 7.5-1e-8)) + 8
    else:
        return round(np.clip(-8 * np.exp(c * x) + 7.5, -0.5+1e-8, 7.5-1e-8))


# 两种压缩成4bit的方式：量化因子法或指数映射的方法
def compress_to_4bit(wave_data, a_or_c, Q, method):
    # 第一个采样值占16bits, 如果不整的话多4bit，值为0
    new_data = np.zeros(int(np.ceil((len(wave_data)-1)/2) + 2), dtype=np.uint8)
    # 把第一个采样值按二进制的前8位和后8位分别存储在new_data[-1]和new_data[0]中
    new_data[-1] = np.int8((wave_data[0] + 32768) // 256)
    new_data[0] = np.int8((wave_data[0] + 32768) % 256)
    # wave_data的索引i, new_data的索引j, ceil(i // 2) = j
    x_ = int(wave_data[0])
    for i in range(1, len(wave_data)):
        j = int(np.ceil(i/2))
        d = int(wave_data[i]) - int(x_)
        c = Q(d, a_or_c)
        if method == 'a':
            x_ += (c - 8) * a_or_c
        elif method == 'e':
            if c >= 8:
                x_ += round(-np.log((7.5 - np.abs(c - 8)) / 8) / a_or_c)
            else:
                x_ += round(np.log((7.5 - np.abs(c)) / 8) / a_or_c)
        if i % 2 == 1:
            new_data[j] = c * 16
        else:
            new_data[j] += c
    if (len(wave_data)-1)/2 % 2 != 0:
        new_data[-2] += 8
    return new_data 


def array_to_file(wave_data, file_name, file_path, extension):
    total_file_name = file_path + file_name + extension
    folder = os.path.exists(file_path)
    if not folder:                 
        os.makedirs(file_path)  
    wave_data.tofile(total_file_name)
    print ('成功生成：' + total_file_name)
        
        
def decompress_8bit(wave_data, a): 
    decompress_data = np.zeros(len(wave_data) - 1, dtype=np.int16)
    decompress_data[0] = (wave_data[0] + 128) + (wave_data[-1] + 128) * 256 - 32768
    for i in range(1, len(decompress_data)):
        decompress_data[i] = decompress_data[i-1] + wave_data[i] * a
    return decompress_data


def decompress_4bit(wave_data, a_or_c, method): 
    decompress_data = np.zeros(2 * (len(wave_data) - 2) + 1, dtype=np.int16)
    decompress_data[0] = wave_data[0] + wave_data[-1] * 256 - 32768
    for i in range(1, len(decompress_data)):
        index = int(np.ceil(i/2))
        if i % 2 == 1:
            c = wave_data[index] // 16
        else:
            c = wave_data[index] % 16
        if method == 'a':
            decompress_data[i] = decompress_data[i-1] + (c - 8) * a_or_c
        elif method == 'e':
            if c >= 8:
                d = round(-np.log((7.5 - np.abs(c - 8)) / 8) / a_or_c)
            else:
                d = round(np.log((7.5 - np.abs(c)) / 8) / a_or_c)
            decompress_data[i] = decompress_data[i-1] + d
    return decompress_data         


def ComputeSNR(wave_data, decompress_data):
    if len(wave_data) != len(decompress_data):
        decompress_data = decompress_data[:-1]
    result = 10 * np.log10((np.linalg.norm(wave_data) ** 2) /
                           (np.linalg.norm(np.abs(wave_data - decompress_data)) ** 2))
    return result
    
        
if __name__ == '__main__':
    for i in range(10):
        filepath = '语料'
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
        wave_data = np.frombuffer(str_data, dtype=np.short)
        f.close()
        
        '''
        a_range = np.linspace(1,2000,501).astype(int)
        SNR_8bit, SNR_4bit = [], []
        for a in a_range:
            compress_8bit_a = compress_to_8bit(wave_data, a)
            decompress_8bit_a = decompress_8bit(compress_8bit_a, a)
            SNR_8bit.append(ComputeSNR(wave_data, decompress_8bit_a))
            compress_4bit_a = compress_to_4bit(wave_data, a, Q_4bit, 'a')
            decompress_4bit_a = decompress_4bit(compress_4bit_a, a, 'a')
            SNR_4bit.append(ComputeSNR(wave_data, decompress_4bit_a))
        
        plt.plot(a_range, SNR_8bit, color='blue', label = '8bit')
        plt.plot(a_range, SNR_4bit, color='darkorange', label = '4bit')
        plt.xlabel('a value')
        plt.xticks(a_range[::20])
        plt.ylabel('SNR')
        plt.legend()
        plt.show()
        
        c_range = np.linspace(0.000015,0.00025,21)
        SNR_e = []
        for c in c_range:
            compress_4bit_e = compress_to_4bit(wave_data, c, Q_e, 'e')
            decompressed_4bit_e = decompress_4bit(compress_4bit_e, c, 'e')
            SNR_e.append(ComputeSNR(wave_data, decompressed_4bit_e))
        
        plt.plot(c_range, SNR_e, color='crimson', label = 'c')
        plt.xlabel('c value')
        plt.xticks(c_range[::6])
        plt.ylabel('SNR')
        plt.legend()
        plt.show()
        '''

        a_8bit, a_4bit = 115, 1600
        compress_8bit = compress_to_8bit(wave_data, a_8bit)
        compress_4bit = compress_to_4bit(wave_data, a_4bit, Q_4bit, 'a')
        
        array_to_file(compress_8bit, '8bit_a', filename[i][:-4] + '/', '.dpc')
        array_to_file(compress_4bit, '4bit_a', filename[i][:-4] + '/', '.dpc')
        
        decompressed_8bit = decompress_8bit(compress_8bit, a_8bit)
        decompressed_4bit = decompress_4bit(compress_4bit, a_4bit, 'a')
        
        array_to_file(decompressed_8bit, '8bit_a', filename[i][:-4] + '/', '.pcm')
        array_to_file(decompressed_4bit, '4bit_a', filename[i][:-4] + '/', '.pcm')

        c = 2.18e-4
        compress_4bit_e = compress_to_4bit(wave_data, c, Q_e, 'e')
        decompressed_4bit_e = decompress_4bit(compress_4bit_e, c, 'e')
        array_to_file(compress_4bit_e, '4bit_e', filename[i][:-4] + '/', '.dpc')
        array_to_file(decompressed_4bit_e, '4bit_e', filename[i][:-4] + '/', '.pcm')
        
        print ()
