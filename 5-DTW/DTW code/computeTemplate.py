import os
import numpy as np
import algorithmTool as AT


def main(template_path, template_num, repeat_num):
    filename = os.listdir(template_path)
    # 存储得到的接近平均长度的平均mfc_array(即返回值)
    final_template = []
    
    for i in range(template_num):
        # 存储同一命令词的10个mfc-array
        mfc_of_1template = []
        # 存储同一命令词的10个mfc-array的长度
        len_array = np.zeros(repeat_num, dtype=int)
        for j in range(repeat_num):
            total_filname = template_path + '/' + filename[i*repeat_num+j]
            mfc_of_1template.append(AT.read_mfc(total_filname))
            len_array[j] = mfc_of_1template[j].shape[0]
            
        ave_len = np.mean(len_array)
        # 选取距离平均长度最近的语音作为临时模板
        ave_index = np.argmin(np.abs(len_array - ave_len))
        # 存储同一命令词的10个mfc-array映射到相同长度ave_len后，存入same_len_mfc
        same_len_mfc = np.zeros((repeat_num, mfc_of_1template[ave_index].shape[0], 
                                 mfc_of_1template[ave_index].shape[1]))
        for j in range(repeat_num):
            if j == ave_index:
                same_len_mfc[j] = np.array(mfc_of_1template[j])
            else:
                cost, path = AT.dtw(mfc_of_1template[ave_index], mfc_of_1template[j])
                same_len_mfc[j] = AT.get_same_len(mfc_of_1template[j], path)
  
        final_template.append(np.mean(same_len_mfc, axis=0))
            
    print('平均模板成功生成！')
    return final_template

