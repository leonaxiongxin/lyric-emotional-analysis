#coding=utf-8
from __future__ import unicode_literals
import re
import json
import getMusicList as gml
import sys
import os
import shutil
import importlib
word_stat = {}
importlib.reload(sys)

try:
    shutil.rmtree('lyric')
    os.makedirs('lyric')
except:
    pass

def getlyricfromurl(str):
    data_json = gml.gethtml('http://music.163.com/api/song/lyric?os=pc&' + str +'&lv=-1&kv=-1&tv=-1')
    data = json.loads(data_json)
    reg = r'[^0-9\[\]\.\:]'
    string = re.compile(reg)
    try:
        lyriclist = re.findall(string, data['lrc']['lyric'])
        str_lrc = ','.join(lyriclist)
        with open('lyric/'+str[3:] + '.txt', 'w+') as file:
            file.write(str_lrc.replace(',', ''))
    except:
        with open('lyric/'+str[3:] + '.txt', 'w+') as file:
            pass

def loadlyricfromfile():
    list_file = os.listdir('lyric')
    temp = {}
    reg = r'\u4f5c\u66f2|\u4f5c\u8bcd'
    lyricre = re.compile(reg)
    fn = open('english_stopword.dat', 'r')
    stopwords = {}.fromkeys([line.rstrip() for line in fn])

    for file_name in list_file:
        temp[file_name] = []
        try:
            with open('lyric/' + file_name, 'r') as lyric:
                if lyric == '':
                    continue
                for line in lyric:
                    line = line.decode().replace('\n', '')
                    temp[file_name].append(line)
            if re.findall(lyricre, temp[file_name][0]) != '':
                del temp[file_name][0]
            if re.findall(lyricre, temp[file_name][0]) != '':
                del temp[file_name][0]
            for item in temp[file_name]:
                temp_1 = item.split(' ')
                for word in temp_1:
                    word = word.lower()
                    if word not in stopwords:
                        if word not in word_stat:
                            word_stat[word] = 1
                        else:
                            word_stat[word] += 1
        except:
            pass

    output = sorted(word_stat.items(), key=lambda item:item[1], reverse=True)
    with open('fin.dat', 'w+') as point:
        for thing in output:
            point.write(str(thing[0]))
            point.write('   ')
            point.write(str(thing[1]))
            point.write('\n')



if __name__ == '__main__':
    print("请输入歌单ID")
    ID = input('Enter:')
    html = gml.gethtml("http://music.163.com/playlist?id=" + ID)
    musiclist = gml.getmusic(html)
    print(musiclist)
    for key in musiclist:
        print(key)
        getlyricfromurl(key)
    loadlyricfromfile()
