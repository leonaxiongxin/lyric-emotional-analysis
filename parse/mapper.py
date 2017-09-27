# -*- coding: utf-8 -*-i
#!/usr/bin/python
import sys
import importlib
import os
import json
from pyltp import Segmentor #分词库ltp
importlib.reload(sys)


model_path = "F:/ltp3.4.0/cws.model" #ltp3.4.0分词模型库
seg = Segmentor()
seg.load(model_path)  #加载分词库


#载入情感词典
def loadDict(fileName,filePath):
        file = os.path.join('%s%s' % (filePath,fileName))
        wordDict = []
        with open(file) as fin:        #情感词典encoding默认状态是gbk
                for line in fin:
                        wordDict.append(str(line.strip()))
        return wordDict


#判断奇偶，在判定否定词权值时使用
def judgeOdd(num):
        if num%2 == 0:
                return 'even'
        else:
                return 'odd'


#遍历原始歌词数据文件夹下的文件
def eachFile(readPath):
        pathDir = os.listdir(readPath)
        for allDir in pathDir:
                child = os.path.join('%s%s' % (readPath,allDir))
                readFile(child)
        print('done')


#读取原始歌词数据文件，分词,计算情感分值
def readFile(fileName):
        with open(fileName,encoding='UTF-8') as fopen:    #ltp分词要求encoding是UTF-8
                #每首歌有一个积极/消极情感值列表
                #遍历每一行（句）歌词作为一个情感单元
                #每一句歌词的[积极情感值,消极情感值]是列表的一项
                count = []     
                for line in fopen:   
                        line = line.strip()
                        words = []
                        words = seg.segment(line)
                        i = 0    #记录扫描到的词的位置
                        a = 0    #记录情感词的位置
                        poscount = 0   #积极情感值
                        negcount = 0   #消极情感值
                        temp = 0       #用于置反时的临时值
                        for word in words:    
                                if word in postDict:
                                        poscount += 1
                                        c = 0
                                        for w in words[a:i]:
                                                if w in degreeDict6:   #扫描积极情感词前的程度词
                                                        poscount *= 6.0
                                                elif w in degreeDict5:
                                                        poscount *= 5.0
                                                elif w in degreeDict4:
                                                        poscount *= 4.0
                                                elif w in degreeDict3:
                                                        poscount *= 3.0
                                                elif w in degreeDict2:
                                                        poscount *= 2.0
                                                elif w in degreeDict1:
                                                        poscount *= 1.0
                                                elif w in inverseDict:
                                                        c += 1
                                        if judgeOdd(c) == 'odd':   #扫描情感词前的否定词数，是否置反
                                                temp = -poscount
                                        poscount += temp
                                        temp = 0
                                        a = i + 1  #情感词位置的变化
                                elif word in negDict:
                                        negcount += 1
                                        d = 0
                                        for w in words[a:i]:
                                                if w in degreeDict6:   #扫描情感词前的程度词
                                                        negcount *= 6.0
                                                elif w in degreeDict5:
                                                        negcount *= 5.0
                                                elif w in degreeDict4:
                                                        negcount *= 4.0
                                                elif w in degreeDict3:
                                                        negcount *= 3.0
                                                elif w in degreeDict2:
                                                        negcount *= 2.0
                                                elif w in degreeDict1:
                                                        negcount *= 1.0
                                                elif w in inverseDict:
                                                        d += 1
                                        if judgeOdd(d) == 'odd':   #扫描情感词前的否定词数，是否置反
                                                temp = -negcount
                                        negcount += temp
                                        a = i + 1  #情感词位置的变化

                                i += 1     #继续向后扫描
                                

                        #以下是情感值出现负数情况下的调整
                        pos = 0
                        neg = 0
                        if poscount < 0 and negcount > 0:
                                neg = negcount - poscount
                                pos = 0
                        elif negcount < 0 and poscount > 0:
                                pos = poscount -negcount
                                neg = 0
                        elif poscount < 0 and negcount < 0:
                                neg = -poscount
                                pos = -negcount
                        else:
                                pos = poscount
                                neg = negcount
                        count.append([pos,neg])
        writeFile(fileName,count)
                                


writePath = "D:/学习文档/一些课件/web智能技术/大作业/process/"
#保存分词、情感分析后的结果
def writeFile(fileName,count):
        name = fileName[32:]
        file = os.path.join('%s%s' % (writePath,name))
        with open(file,'w') as fw:
                for c in count:
                        fw.write(','.join(str(i) for i in c) + '\n')


dictPath = 'D:/学习文档/一些课件/web智能技术/大作业/parse/sentimentDict/'
postDict = loadDict('positive.txt',dictPath)
negDict = loadDict('negative.txt',dictPath)
inverseDict = loadDict('inverse.txt',dictPath)
degreeDict1 = loadDict('程度级别1词语（中文）.txt',dictPath)
degreeDict2 = loadDict('程度级别2词语（中文）.txt',dictPath)
degreeDict3 = loadDict('程度级别3词语（中文）.txt',dictPath)
degreeDict4 = loadDict('程度级别4词语（中文）.txt',dictPath)
degreeDict5 = loadDict('程度级别5词语（中文）.txt',dictPath)
degreeDict6 = loadDict('程度级别6词语（中文）.txt',dictPath)


if __name__ == '__main__':
        readPath = "D:/学习文档/一些课件/web智能技术/大作业/origin/"
        eachFile(readPath)
        
