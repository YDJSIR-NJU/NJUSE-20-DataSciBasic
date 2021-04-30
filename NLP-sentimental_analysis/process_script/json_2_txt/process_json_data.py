import json
data = []
with open('../../raw_data/peopledailyfinal.json','r',encoding='utf-8') as f:
   data =  json.load(f)


del data[0]



import codecs
count = 0
for i in range(len(data)):
    if count >= 10:
        break
    if not ((data[i]["微博内容"].find("疫") == -1)):
        count = count+1
        for j in range(len(data[i]["评论"])):
            comment_str = data[i]["评论"][j]
            print(comment_str)
            jug = input('上面的评论是pos则输入f，反之输入j,不然则废弃')
            if jug == 'f':
                file_object = codecs.open('../../raw_data/tagged_data/pos_yiqing/pos.{0}.{1}.txt_utf8'.format(i + 1, j + 1), 'w', "utf-8")
                file_object.write(comment_str)
                file_object.close()
            elif (jug == 'j'):
                file_object = codecs.open('../../raw_data/tagged_data/neg_yiqing/neg.{0}.{1}.txt_utf8'.format(i + 1, j + 1), 'w', "utf-8")
                file_object.write(comment_str)
                file_object.close()
            else:
                continue
