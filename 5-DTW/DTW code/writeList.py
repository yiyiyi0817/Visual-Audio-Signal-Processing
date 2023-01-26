import os 

# 写hcopy所需要的list.scp文件
def main(train_path, wave_path, mfcc_path):
    filepath = train_path + '/' + wave_path
    savepath = train_path + '/' + mfcc_path
    folder = os.path.exists(savepath)
    if not folder:                 
        os.makedirs(savepath)            
    filenames = os.listdir(filepath)
    with open(train_path + '/' + 'list.scp', 'w') as f:
        for filename in filenames:
            f.write(str(filepath) + '/' + str(filename) + ' ' 
                    + str(savepath) + '/' + str(filename)[:-4] + '.mfc' +'\n')
    print ('成功保存:list.scp')
    f.close()