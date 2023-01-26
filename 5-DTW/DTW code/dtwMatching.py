import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import algorithmTool as AT


# 根据模板和阈值返回待检测文件的标签
def match(template, test_mfc_filename, threshold):
    test_mfc_array = AT.read_mfc(test_mfc_filename)
    cost_lst = np.zeros(len(template))
    
    for i in range(len(template)):
        cost, path = AT.dtw(template[i], test_mfc_array)
        cost_lst[i] = cost
    
    if np.min(cost_lst) <= threshold:
        return np.argmin(cost_lst) + 1, cost_lst
    else:
        return 0, cost_lst


# 观察cost值在正确匹配和错误匹配下的大小
def computeThreshold(template, folder_path1, folder_path2):
    filename1 = os.listdir(folder_path1)
    filename2 = os.listdir(folder_path2)
    right_cost = []
    wrong_cost = []
    for i in range(len(filename1)):
        total_filname = folder_path1 + '/' + filename1[i]
        pred, cost_lst = match(template, total_filname, sys.maxsize)
        if i < 6:
            wrong_cost.extend(cost_lst)
        elif i < len(filename1):
            right_cost.append(cost_lst[pred-1])
            np.delete(cost_lst, pred - 1)
            wrong_cost.extend(cost_lst)
            
    for i in range(len(filename2)):
        total_filname = folder_path2 + '/' + filename2[i]
        pred, cost_lst = match(template, total_filname, sys.maxsize)
        right_cost.append(cost_lst[pred-1])
        np.delete(cost_lst, pred - 1)
        wrong_cost.extend(cost_lst)
        
    d = np.linspace(20,30,51)
    plt.xticks(d[::3])
    plt.hist(wrong_cost, d, color='orange')
    plt.title('wrong and right')
    plt.hist(right_cost, d, color='blue')    
    plt.show()
        

# 根据模板和阈值，计算文件夹中待检测文件的正确识别率
def match_all(template, folder_path, threshold):
    filename = os.listdir(folder_path)
    right_sum = 0
    for i in range(len(filename)):
        total_filname = folder_path + '/' + filename[i]
        pred, _ = match(template, total_filname, threshold)
        #print (pred)
        if str(pred) == filename[i][0]:
            right_sum += 1
    print (right_sum)
    print (right_sum / len(filename))
    
    