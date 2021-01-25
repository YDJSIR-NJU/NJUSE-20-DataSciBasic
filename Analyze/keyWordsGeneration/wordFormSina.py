from jieba import analyse
from pyecharts import options as opts
from pyecharts.charts import WordCloud
import math
import os
import re
import Date
import time
import stage
import json

path = 'sinaTitles/'
stageNo = 6
# path = stage.stage[stageNo]['path']
beginDate = stage.stage[stageNo]['beginDate']
print(beginDate)
endDate = stage.stage[stageNo]['endDate']
print(endDate)
date = '1970-01-01-'
textrank = analyse.textrank

ExtraStopWords = ['荔枝', '新闻', 'trog', '投资者', '黑猫', '投诉']


def run():
    # generateTexts()
    # generateWords()
    # date = beginDate
    # while True:
    #     os.mkdir('sinaTitles/' + str(date))
    #     date = Date.getNextDate(date)
    #     if Date.dateCmp(date, endDate) == 1:
    #         break
    genStageWordCloud()


def generateTexts():
    print('Begin')
    try:
        os.mkdir('sinaTitles')
    except Exception as e:
        print(e)
    path = 'sina2019/'

    fp = open('sinaTitles/stage1News2019_sina.csv', 'r', encoding='utf-8')

    tmpDayContent = ''
    date = beginDate
    fp3 = open('sinaTitles/begin.data', 'w', encoding='utf-8')
    while True:
        tmpLine = fp.readline().strip()
        if tmpLine == '':
            break
        tmpItems = tmpLine.split(',')
        length = len(tmpItems)
        curDate = str(tmpItems[length - 1]) + '-'
        if Date.dateCmp(curDate, date) != 0:
            fp3.write(tmpDayContent)
            tmpDayContent = ''
            print(str(date) + ' Finished')
            date = curDate
            try:
                os.mkdir('sinaTitles/' + str(date))
            except:
                print('e')
            fp3 = open(('sinaTitles/' + date + '/' + date + 'words.txt'), 'w', encoding='utf-8')
            # + date + '/'
        else:
            tmpDayContent += str(tmpItems[0])

    fp = open('sinaTitles/stage1News2019_sina_title.csv', 'r', encoding='utf-8')
    fp3 = open('sinaTitles/begin.data', 'a+', encoding='utf-8')
    while True:
        tmpLine = fp.readline().strip()
        print(tmpLine)
        if tmpLine == '':
            break
        tmpItems = tmpLine.split(',')
        length = len(tmpItems)
        curDate = str(tmpItems[length - 1]) + '-'
        if Date.dateCmp(curDate, date) != 0:
            fp3.write(tmpDayContent)
            fp3.flush()
            tmpDayContent = ''
            print(str(date) + ' Finished')
            date = curDate
            fp3 = open(('sinaTitles/' + date + 'words.txt'), 'a+', encoding='utf-8')
            # + date + '/'
        else:
            tmpDayContent += str(tmpItems[0])


def generateWords():
    tmpDayContent = ''
    date = '2019-12-25-'
    fp = open(('sinaTitles/' + str(date) + 'words.txt'), 'r', encoding='utf-8')
    fp3 = open('sinaTitles/' + str(date) + 'keywords.json', 'w', encoding='utf-8')
    while True:
        tmpLine = fp.readline().strip()
        print(tmpLine)
        if tmpLine == '':
            keywords = textrank(tmpDayContent, topK=36, withWeight=True, withFlag=True)
            print(keywords)
            words = []
            for item in keywords:
                a = list()
                items = str()
                curWord = str(item[0]).split('/')[0]
                if curWord in ExtraStopWords:
                    continue
                a.append(curWord)
                a.append(math.floor((item[1] * 100)))
                words.append(tuple(a))
            # print(words)
            wordcloud_base(words).render('sinaTitles/' + date + '/' + date + 'keywords.html')
            wordsS = json.dumps(words, indent=4, separators=(',', ':'), ensure_ascii=False)
            fp3.write(wordsS)
            fp3.flush()
            tmpDayContent = ''
            print(str(date) + ' Finished')
            date = Date.getNextDate(date)
            if Date.dateCmp(date, endDate) == 1:
                break
            fp3 = open(('sinaTitles/' + date + '/' + date + 'keywords.json'), 'w', encoding='utf-8')
            fp = open(('sinaTitles/' + date + '/' + date + 'words.txt'), 'r', encoding='utf-8')
            # print('sleep')
            # time.sleep(2)
        else:
            tmpDayContent += str(tmpLine)


def genStageWordCloud():
    with open(stage.stage[stageNo]['path'] + '/COVkeywords-' + stage.stage[stageNo]['Path'] + '-.json', 'r', encoding='utf-8') as fp:
        words = json.load(fp)

        # words = [(math.floor(x[1]) * 100) for x in words]
        print(words)
        c = wordcloud_base(words)
        wordcloud_base(words).render(stage.stage[stageNo]['path'] + '/COVkeywords-' + stage.stage[stageNo]['Path'] + '-.html')


def wordcloud_base(words) -> WordCloud:
    c = (
        WordCloud()
            .add("", words, word_size_range=[20, 100], shape='roundRect')  # SymbolType.ROUND_RECT
            .set_global_opts(title_opts=opts.TitleOpts(title='WordCloud词云'))
    )
    return c


if __name__ == "__main__":
    run()
