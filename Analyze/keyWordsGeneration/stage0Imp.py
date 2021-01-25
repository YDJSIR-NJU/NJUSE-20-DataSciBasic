import numpy as np
import matplotlib.pyplot as plt
import math
import os
import re
import Date
import time
import json
import jieba
import stage
import splitWeibo
from scipy.optimize import curve_fit
from scipy.stats import chi2_contingency

stageNo = 0
path = stage.stage[stageNo]['path']
beginDate = stage.stage[stageNo]['beginDate']
print(beginDate)
endDate = stage.stage[stageNo]['endDate']
print(endDate)
date = '1970-01-01-'

keywords = []
scoreList = []
starList = []
forwardList = []
commentList = []
allWeibo = []
weiboNumByDate = []
COVWeiboNumList = []
ka = []


# textrank = analyse.textrank

def run():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    keywords = keywordsInit()
    print('Begin')
    # 根据微博正文给所有微博打分
    date = beginDate
    while Date.dateCmp(date, endDate) != 1:
        getWeiboScores(date, keywords)
        readScoreWords(date)
        print(date + 'Finished')
        date = Date.getNextDate(date)
    global scoreList
    numOfWeibo = len(scoreList)

    limit = fitData()  # 第二、第三阶段fit出来都很完美，第一阶段fit不出来的
    drawPic()

    COVWeiboList = [weibo for weibo in allWeibo if weibo['疫情相关度'] > limit]
    for item in COVWeiboList:
        item['是否与疫情相关'] = True
    COVWeiboNum = len(COVWeiboList)

    print(weiboNumByDate)
    fp = open(path + '/' + 'stageInfo.json', mode='w', encoding='utf-8')
    stageInfo = {'微博数量': numOfWeibo, '疫情相关微博数量': COVWeiboNum, '卡方检验': str(ka)}
    # stage['疫情信息热度'] = 0
    outWeiboInfo = json.dumps(stageInfo, indent=4, separators=(',', ':'), ensure_ascii=False)
    fp.write(outWeiboInfo)
    fp.flush()

    fp = open(path + '/' + 'stageCOVWeibo.json', mode='w', encoding='utf-8')
    outCOVWeibo = json.dumps(COVWeiboList, indent=4, separators=(',', ':'), ensure_ascii=False)
    fp.write(outCOVWeibo)
    fp.flush()

    fp = open(path + '/' + 'stageCOVWeiboByImportance.json', mode='w', encoding='utf-8')
    COVWeiboList = sorted(COVWeiboList, key=lambda x: x['疫情相关度'], reverse=True)
    time.sleep(3)
    print('stageCOVWeiboByImportance.json')
    outCOVWeiboByImportance = json.dumps(COVWeiboList, indent=4, separators=(',', ':'), ensure_ascii=False)
    fp.write(outCOVWeiboByImportance)
    fp.flush()

    splitWeibo()


def getWeiboScores(date, keywords):
    i = 0
    fp = open(path + '/' + date + '/' + date[0:10] + 'info.json', mode='r', encoding='utf-8')
    curDateWeibo = json.load(fp)
    weiboNumByDate.append(len(curDateWeibo))
    for weibo in curDateWeibo:
        content = weibo['微博内容']
        # print(content)
        contentWordList = jieba.cut(content)
        score = 0
        keywordsWithoutWeight = [x[0] for x in keywords]
        for word in contentWordList:
            if word in keywordsWithoutWeight:
                score += keywords[keywordsWithoutWeight.index(word)][1]
        i += 1
        weibo['疫情相关度'] = score
        weibo['是否与疫情相关'] = False
        # print(score)
        scoreList.append(score)
        forwardList.append(weibo['转发数'])
        starList.append(weibo['点赞数'])
        commentList.append(weibo['评论数'])
        weibo['评论'] = weibo['评论'][0:math.floor(len(weibo['评论']) / 5)]
        # if i > 2:
        #     break
        allWeibo.append(weibo)
    fp = open(path + '/' + date + '/' + date + 'blog-Scored.json', mode='w', encoding='utf-8')
    outCurDateWeibo = json.dumps(curDateWeibo, indent=4, separators=(',', ':'), ensure_ascii=False)
    fp.write(outCurDateWeibo)

    # 生成当日微博基础信息，可能后面有增补
    fp = open(path + '/' + date + '/' + date + 'blogInfo.json', mode='w', encoding='utf-8')
    curDateWeiboInfo = {}
    curDateWeiboInfo['微博数量'] = len(curDateWeibo)
    curDateWeiboInfo['疫情相关微博数量'] = 0
    # curDateWeiboInfo['疫情信息热度'] = 0
    outWeiboInfo = json.dumps(curDateWeiboInfo, indent=4, separators=(',', ':'), ensure_ascii=False)
    fp.write(outWeiboInfo)
    fp.flush()


def readScoreWords(date):
    i = 0
    fp = open(path + '/' + date + '/' + date + 'blog-Scored.json', mode='r', encoding='utf-8')
    curDateWeibo = json.load(fp)
    weiboNumByDate.append(len(curDateWeibo))
    allWeiboNeedReload = False
    if allWeibo == {}:
        allWeiboNeedReload = True
    for weibo in curDateWeibo:
        content = weibo['微博内容']
        scoreList.append(weibo['疫情相关度'])
        starList.append(weibo['点赞数'])
        forwardList.append(weibo['转发数'])
        commentList.append(weibo['评论数'])
        if allWeiboNeedReload:
            allWeibo.append(weibo)
    weiboNumByDate.append(len(curDateWeibo))
    fp = open(path + '/' + date + '/' + date + 'blogInfo.json', mode='r', encoding='utf-8')
    curDateWeiboInfo = json.load(fp)
    # COVWeiboNumList.append(curDateWeiboInfo['疫情相关微博数量'])
    # print('当天疫情相关微博数量' + str(curDateWeiboInfo['疫情相关微博数量']))


def fitData():
    xplot = np.arange(1, len(scoreList) + 1)
    scoreListN = np.array(sorted(scoreList))
    popt, pcov = curve_fit(exponent, xplot, scoreListN)
    plt.plot(xplot, sorted(scoreList), 'b+:', label='原始相关度')
    fitedData = exponent(xplot, *popt)

    limit1 = np.percentile(fitedData, stage.stage[stageNo]['ratio'])
    # limit1 = np.percentile(fitedData, 99.5)
    fitedLine = [exponent(x, popt[0], popt[1], popt[2], popt[3]) for x in xplot]
    plt.axhline(y=limit1, color="purple")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(xplot, fitedData, linestyle="-", marker="", color='r', label='拟合曲线')
    plt.legend()
    plt.savefig(path + '/SaveTest_Fit.png', dpi=300)
    global ka
    ka = chi2_contingency(np.asarray([scoreListN, fitedData]))
    return limit1
    # averageScore = average


def drawPic():
    # 绘图部分
    print()
    global scoreList
    xplot = [x for x in range(1, len(scoreList) + 1)]
    scoreList = sorted(scoreList)
    # plt.scatter(xplot, scoreList, s=2, color="r", marker=".", linewidth=1, alpha=0.3, label='疫情相关度')
    starList1 = [math.log10(x + 1) * 15 for x in starList]
    commentList1 = sorted([math.log10(x + 1) * 8 for x in commentList])
    forwardList1 = [math.log10(x + 1) * 10 for x in forwardList]
    # plt.plot(xplot, starList1, color="g", linestyle="", marker="^", linewidth=1, label='点赞数')
    plt.plot(xplot, commentList1, color="y", linestyle="", marker=".", linewidth=1, alpha=0.1, label='评论数')
    # plt.plot(xplot, forwardList1, color="y", linestyle="", marker="^", linewidth=1, label='转发数')
    plt.rcParams['figure.dpi'] = 300
    plt.xlabel = '微博数量（从左到右递增）'
    plt.legend()
    plt.savefig(path + '/SaveTest.png', dpi=300)
    # plt.show()


# 正态分布的函数表达式
def gaussian(x, *param):
    return param[1] * np.exp(-np.power(x - param[0], 2.) / (2 * np.power(param[1], 2.)))


# 正态分布的函数表达式
def exponent(x, a, b, c, d):
    return a * np.power(b, (x - d)) + c


def keywordsInit():
    # with open(stage.stage[stageNo]['path'] +'/keywords-' + stage.stage[stageNo]['Path'] +'.json', mode='r', encoding='utf-8') as fp:
    #     keywords = json.load(fp)
    #     keywords = sorted(keywords, key=lambda s: s[1], reverse=True)
    #     maxNum = math.log10(keywords[0][1])
    #     for item in keywords:
    #         item[1] = math.log10(item[1])
    #         item[1] = item[1] / maxNum
    #     newWords = json.dumps(keywords, indent=4, separators=(',', ':'), ensure_ascii=False)
    #     with open(stage.stage[stageNo]['path'] +'/COVkeywords-' + stage.stage[stageNo]['Path'] +'.json', mode='w', encoding='utf-8') as fp2:
    #         fp2.write(newWords)
    #         fp2.flush()
    with open(stage.stage[stageNo]['path'] + '/COVkeywords-' + stage.stage[stageNo]['Path'] + '-.json', mode='r',
              encoding='utf-8') as fp2:
        # print(fp2.read())
        keywords = json.loads(str(fp2.read()))
    return keywords


def getSingleBlog(fp):
    blog = ""
    tmp = fp.readline()
    if tmp[0] == '{':
        while tmp[0] != '}':
            blog = blog + tmp
            tmp = fp.readline()
        blog += '}'
    return blog


def splitWeibo():
    date = beginDate
    with open(path + '/stageCOVWeibo.json', mode='r', encoding='utf-8') as fp:
        allCovWeibo_ = json.load(fp)
        allCovWeibo = sorted(allCovWeibo_, key=lambda x: x['发布时间'])
        fp2 = open(path + '/' + date + '/' + date + 'blog-COV.json', 'w+', encoding='utf-8')
        fp2.write('[\n')
        numOfDate = 0
        numOfCurDateCOVWeibo = 0
        numOfCOVWeibo = len(allCovWeibo)
        dailyCOVWeiboRatioList = []
        for i in range(0, numOfCOVWeibo):
            # print(i)
            if (allCovWeibo[i]['发布时间'] + '-') == date:
                weiboS = json.dumps(allCovWeibo[i], indent=4, separators=(',', ':'), ensure_ascii=False)
                fp2.write(weiboS)
                if i != (numOfCOVWeibo - 1) and (
                        (i + 1) <= (numOfCOVWeibo - 1) and (allCovWeibo[i + 1]['发布时间'] + '-') == date):
                    # print('next ' + allCovWeibo[i + 1]['发布时间']+'-')
                    fp2.write(',\n')
                else:
                    # print('NO,')
                    fp2.write('\n')
                numOfCurDateCOVWeibo += 1
            else:
                fp2.write(']')
                fp3 = open(path + '/' + date + '/' + date + 'blogInfo.json', mode='r', encoding='utf-8')
                curDateWeiboInfo = json.load(fp3)
                curDateWeiboInfo['疫情相关微博数量'] = numOfCurDateCOVWeibo
                # curDateWeiboInfo['疫情信息热度'] = 0
                curDateWeiboInfo['疫情相关微博占比'] = numOfCurDateCOVWeibo / curDateWeiboInfo['微博数量']
                dailyCOVWeiboRatioList.append(curDateWeiboInfo['疫情相关微博占比'])
                print(dailyCOVWeiboRatioList)
                COVWeiboNumList.append(numOfCurDateCOVWeibo)
                numOfCurDateCOVWeibo = 0
                outWeiboInfo = json.dumps(curDateWeiboInfo, indent=4, separators=(',', ':'), ensure_ascii=False)
                fp3 = open(path + '/' + date + '/' + date + 'blogInfo.json', mode='w', encoding='utf-8')
                fp3.write(outWeiboInfo)
                fp3.flush()
                print(date + ' Finished')
                # break
                date = allCovWeibo[i]['发布时间'] + '-'
                fp2 = open(path + '/' + date + '/' + date + 'blog-COV.json', 'w+', encoding='utf-8')
                fp2.write('[\n')
                weiboS = json.dumps(allCovWeibo[i], indent=4, separators=(',', ':'), ensure_ascii=False)
                fp2.write(weiboS)
                if i != (numOfCOVWeibo - 1) or (
                        (i + 1) <= (numOfCOVWeibo - 1) and (allCovWeibo[i]['发布时间'] + '-') != date):
                    fp2.write(',\n')
                else:
                    # print('NO,')
                    fp2.write('\n]')
                numOfDate += 1
                # if numOfDate > 3:
                #     break
        try:
            fp3 = open(path + '/' + date + '/' + date[0:10] + 'blogInfo.json', mode='r', encoding='utf-8')
            curDateWeiboInfo = json.load(fp3)
            curDateWeiboInfo['疫情相关微博数量'] = numOfCurDateCOVWeibo
            curDateWeiboInfo['疫情相关微博占比'] = numOfCurDateCOVWeibo / curDateWeiboInfo['微博数量']
            COVWeiboNumList.append(numOfCurDateCOVWeibo)
            dailyCOVWeiboRatioList.append(curDateWeiboInfo['疫情相关微博占比'])
            outWeiboInfo = json.dumps(curDateWeiboInfo, indent=4, separators=(',', ':'), ensure_ascii=False)
            fp3 = open(path + '/' + date + '/' + date + 'blogInfo.json', mode='w', encoding='utf-8')
            fp3.write(outWeiboInfo)
            fp3.flush()
            print(date + ' Finished')
        except Exception as e:
            print(e)

        # 绘图
        plt.clf()
        llen = len(dailyCOVWeiboRatioList) + 1
        xplot = [x for x in range(1, llen)]
        dailyCOVWeiboRatioList_ = [x * 100 for x in dailyCOVWeiboRatioList]
        plt.xticks(np.arange(0, llen + 2, 2))
        plt.plot(xplot, dailyCOVWeiboRatioList_, color="r", marker=".", linewidth=1, alpha=0.7, label='疫情相关微博百分比')
        for a, b in zip(xplot, dailyCOVWeiboRatioList_):
            plt.text(a, b, (a, round(b, 2)), ha='center', va='bottom', fontsize=10)
        # global COVWeiboNumList
        # print('ANALYSE')
        # print(xplot)
        # print(COVWeiboNumList)
        plt.plot(xplot, COVWeiboNumList, color="g", marker=".", linewidth=1, alpha=0.7, label='疫情相关微博数量')
        plt.legend()
        plt.savefig(path + '/ratioByDate.png', dpi=300)


if __name__ == "__main__":
    # keywordsInit()
    # print(exponent(2, 5, 6))
    run()
    # splitWeibo()
