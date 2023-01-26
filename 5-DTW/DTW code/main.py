import endPointDetection
import writeList
import computeTemplate
import dtwMatching
import sys

if __name__ == '__main__':
    endPointDetection.main(50, '语料', 'pcm/')
    endPointDetection.main(21, '测试集', 'pcm_test/')
    
    hcopy_path = 'C:/Users/Lenovo/Desktop/视听觉信号处理/实验/听觉3/MFCC提取工具'
    writeList.main(hcopy_path, 'wave', 'mfcc')
    writeList.main(hcopy_path, 'wave_test', 'mfcc_test')
    
    # 中间提取mfcc特征部分用hcopy命令行处理，程序分段进行
    
    Template = computeTemplate.main('MFCC提取工具/mfcc', 5, 10)
    dtwMatching.computeThreshold(Template, 'MFCC提取工具/mfcc_test', 'MFCC提取工具/mfcc')
    dtwMatching.match_all(Template, 'MFCC提取工具/mfcc_test', 27)

    