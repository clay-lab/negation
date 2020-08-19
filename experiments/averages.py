import os
from sys import argv
from statistics import mean
import csv

def main():
    dicts1 = os.path.join(argv[1], "model-1", "dicts.csv")
    dicts2 = os.path.join(argv[1], "model-2", "dicts.csv")
    dicts3 = os.path.join(argv[1], "model-3", "dicts.csv")
    dicts4 = os.path.join(argv[1], "model-4", "dicts.csv")
    dicts5 = os.path.join(argv[1], "model-5", "dicts.csv")
    avgdicts = os.path.join(argv[1], "AverageDicts.csv")
    with open(dicts1, 'r') as dicts1file, open(dicts2, 'r') as dicts2file, open(dicts3, 'r') as dicts3file, open(dicts4, 'r') as dicts4file, open(dicts5, 'r') as dicts5file, open(avgdicts, 'w') as avgfile:
        dicts1list = list(csv.reader(dicts1file, delimiter='\t', lineterminator='\n'))
        dicts2list = list(csv.reader(dicts2file, delimiter='\t', lineterminator='\n'))
        dicts3list = list(csv.reader(dicts3file, delimiter='\t', lineterminator='\n'))
        dicts4list = list(csv.reader(dicts4file, delimiter='\t', lineterminator='\n'))        
        dicts5list = list(csv.reader(dicts5file, delimiter='\t', lineterminator='\n'))
        avgwriter = csv.writer(avgfile, delimiter=',', lineterminator='\n')
        dictnum = len(list(dicts1list))
        collatedDicts = []
        for i in range(dictnum):
            collatedDicts.append([dicts1list[i][0].split(',')[1:],dicts2list[i][0].split(',')[1:], dicts3list[i][0].split(',')[1:], dicts4list[i][0].split(',')[1:], dicts5list[i][0].split(',')[1:]])
        for i in range(dictnum):
            # take percentages off
            if '%' in collatedDicts[i][0][1]:
                for j in range(5):
                    for k in range(len(collatedDicts[i][j])):
                        collatedDicts[i][j][k] = float(collatedDicts[i][j][k].strip('%')) / 100
            # turn them into numbers
            else:
                for j in range(5):
                    for k in range(len(collatedDicts[i][j])):
                        collatedDicts[i][j][k] = int(collatedDicts[i][j][k])
        meanDicts = []
        for i in range(dictnum):
            meandict = []
            for j in range(len(collatedDicts[0][0])):
                meandict.append(round(mean([collatedDicts[i][0][j], collatedDicts[i][1][j], collatedDicts[i][2][j], collatedDicts[i][3][j], collatedDicts[i][4][j]]), 2))
            meanDicts.append(meandict)  
        dictnames = [dicts1list[i][0].split(',')[0] for i in range(dictnum)]
        for i in range(dictnum):
            meanDicts[i].insert(0, dictnames[i])
            avgwriter.writerow(meanDicts[i])

main()
