import codecs
import json
import os
#26天 60个相关话题 300条评论
filenames = []
stage_path = './raw_data/stage3_json'
count = 0
filenames = os.listdir(stage_path)
for file in filenames: # file 是文件夹名 如 2020-02-21-
    if  os.path.isdir(os.path.join(stage_path, file)): # 是目录
        current_file = os.path.join(stage_path, file, file+'blog.json') #目录下的目标文件
        with open(current_file,'r', encoding='utf-8') as f:
            data = []
            data = json.load(f)
            # print(len(data))
            for i in range(len(data)):
                for j in range(min(len(data),10)): # 给前十条评论打标签
                    comment_str = data[i]["评论"][j]
                    print(comment_str)
                    jug = input('上面的评论是pos则输入q，反之输入w,不然则废弃')
                    if jug == 'q':
                        target_dir = './raw_data/tagged_data/stage3_txt/{0}/pos_yiqing'.format(file)
                        if not os.path.exists(target_dir):
                            os.makedirs(target_dir)
                        file_object = codecs.open(target_dir+'/pos.{0}.{1}.txt_utf8'.format(i+1,j+1), 'w', "utf-8")
                        file_object.write(comment_str)
                        file_object.close()
                    elif (jug == 'w'):
                        target_dir = './raw_data/tagged_data/stage3_txt/{0}/neg_yiqing'.format(file)
                        if not os.path.exists(target_dir):
                            os.makedirs(target_dir)
                        file_object = codecs.open(target_dir+'/pos.{0}.{1}.txt_utf8'.format(i+1,j+1), 'w', "utf-8")
                        file_object.write(comment_str)
                        file_object.close()
                    else:
                        continue