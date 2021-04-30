import pickle
import jieba
import os
import re
import string

pos_words = []
neg_words = []




# FindPath = '../../raw_data/tagged_data/pos_yiqing/'
FindPath = '../../raw_data/tagged_data/stage3_txt/2020-02-21-/pos_yiqing'

FileNames = os.listdir(FindPath)
num_of_pos_filep = len(FileNames)
for file_name in FileNames:
    full_file_name = os.path.join(FindPath, file_name)
    if 'utf8' in full_file_name:
        with open(full_file_name, 'r', encoding='utf-8') as pos_f:
            pos_text = pos_f.read()
            pos_text = ''.join(pos_text.split())
            pos_text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）～-]+", "", pos_text) # 去除标点符号
            pos_list = jieba.cut(pos_text, cut_all=False)
            pos_words.append(list(pos_list))


# FindPath = '../../raw_data/tagged_data/neg_yiqing/'
FindPath = '../../raw_data/tagged_data/stage3_txt/2020-02-21-/neg_yiqing'

FileNames = os.listdir(FindPath)
num_of_neg_file = len(FileNames)
for file_name in FileNames:
    full_file_name = os.path.join(FindPath, file_name)
    if 'utf8' in full_file_name:
        with open(full_file_name, 'r', encoding='utf-8') as neg_f:
            neg_text = neg_f.read()
            neg_text = ''.join(neg_text.split())
            # neg_text = re.sub(string.punctuation, "", neg_text)
            neg_text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）～-]+", "", neg_text)
            neg_list = jieba.cut(neg_text, cut_all=False)
            neg_words.append(list(neg_list))




# output = open('../../pkl_data/tagged_data/pos_comment.pkl', 'wb')
output = open('../../pkl_data/tagged_data/pos_comment_oneday.pkl', 'wb')

pickle.dump(pos_words[:min(num_of_pos_filep,num_of_neg_file)], output)
output.close()

# output = open('../../pkl_data/tagged_data/neg_comment.pkl', 'wb')
output = open('../../pkl_data/tagged_data/neg_comment_oneday.pkl', 'wb')

pickle.dump(neg_words[:min(num_of_pos_filep,num_of_neg_file)], output)
output.close()
