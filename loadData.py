# -*- coding: utf-8 -*-i
#!/usr/bin/python
import numpy as np
import os

def main():
    readPath = "D:/学习文档/一些课件/web智能技术/大作业/process/"
    fdata = open("D:/学习文档/一些课件/web智能技术/大作业/data.txt",'wb')
    pathDir = os.listdir(readPath)
    count = []
    for allDir in pathDir:
        child = os.path.join('%s%s' % (readPath,allDir))
        with open(child) as fopen:
            for line in fopen:
                if line.strip() not in count:
                    count.append(line.strip())
                else:
                    pass
    data = np.zeros((192,110))
    i = 0
    for allDir in pathDir:
        child = os.path.join('%s%s' % (readPath,allDir))
        with open(child) as fopen:
            for line in fopen:
                j = count.index(line.strip())
                data[i,j] += 1
        i += 1
    np.savetxt(fdata, data, fmt='%d',delimiter='\t')

    fdata.close()
    print("done")

               
if __name__ == '__main__':
    main()
