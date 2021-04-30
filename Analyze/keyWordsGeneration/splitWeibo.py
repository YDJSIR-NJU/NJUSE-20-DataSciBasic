"""
    分割微博到对应路径中
"""

import json
import os
import time
import stage
import Date

stageNo = 0
# path = stage.stage[stageNo]['path']
path = 'jstv'
beginDate = stage.stage[stageNo]['beginDate']
print(beginDate)
endDate   = stage.stage[stageNo]['endDate']
print(endDate)
date = '1970-01-01-'

def getTitle(fp):
    print("Get Blogger Info")
    header = ""
    fp.readline()
    for i in range(0, 7):
        header = header + (fp.readline())
    header += '}'
    fp.readline()
    # try:
    #     os.makedirs(path + "/" + json.loads(header)['微博用户名'])
    # except Exception as e :
    #     print(e)
    # with open(path + "/" + date + , mode='w', encoding='utf-8') as fp2:
    #     fp2.write(header)
    #     fp2.flush()
    return json.loads(header)['微博用户名']

    # fp2.write('\n')


# def getBlogOf1Day(fp):
#     # 读取单日的所有博客
#     # print('GetBlogTest')
#     while True:
#         curBlog = getSingleBlog(fp)
#
#     fileNameAndPath = str('SplitedWeibo/' + content['发布时间'] + '_info.json'):
#     with open(fileNameAndPath, 'w', encoding='utf-8') as fp2:
#         fp2.write(blog)
#         fp2.flush()
#     return extra

def getSingleBlog(fp):
    blog = ""
    tmp = fp.readline()
    if tmp[0] == '{':
        while tmp[0] != '}':
            blog = blog + tmp
            tmp = fp.readline()
        blog += '}'
    return blog


if __name__ == "__main__":
    with open('peopledailyfianl.json', 'r', encoding='utf-8') as fp:
        bloggerName = getTitle(fp)
        date = ""
        pathOfBlogger = str(path + "/" + 'BeginSplitWeibo.data')
        fp2 = open(pathOfBlogger, 'w', encoding='utf-8')
        numOfDate = 0
        while True:
            curBlog = getSingleBlog(fp)
            curBlogContent = {}
            try:
                curBlogContent = json.loads(curBlog)
            except Exception as e:
                print("No more blogs!")
                break
            # if Date.dateCmp((curBlogContent['发布时间'] + '-'), endDate) == 1 or Date.dateCmp((curBlogContent['发布时间'] + '-'), endDate) == -1:
                # print(str(stageNo) + 'stage Finished')
                # break
            #     continue
            if (date != curBlogContent['发布时间']):
                numOfDate += 1
                if date == '':
                    print('Begin')
                else:
                    fp2.write('\n]')
                    print(date + " Finished!")
                try:
                    fp2 = open(path + '/' + curBlogContent['发布时间'] + '-/' + curBlogContent['发布时间'] + '-blog.json', 'w',
                               encoding='utf-8')
                except Exception as e:
                    print(e)
                    continue
                date = curBlogContent['发布时间']
                print(curBlogContent['发布时间'])
                fp2.write('[\n')
                fp2.write(curBlog)
            else:
                fp2.write(',\n')
                fp2.write(curBlog)
            fp2.flush()
            # time.sleep(1)
            # if numOfDate > 2:
            #     break
