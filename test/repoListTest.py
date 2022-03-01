#f = open('data2/processed_python_output102','r')
import os

badRepoList = []

lineCounter = 0
goodCounter = 0
badCounter = 0
dataDir = 'data/'

for files in filter(lambda l: 'processed' in l, os.listdir(dataDir)):
    for line in open(dataDir+files, 'r'):
        lineCounter += 1
        if line.split(':')[1] == '\n':
            badRepoList.append((line.split(':')[0],files))
            badCounter +=1
        else:
            goodCounter += 1
print(badRepoList)
print(lineCounter, goodCounter, badCounter)
