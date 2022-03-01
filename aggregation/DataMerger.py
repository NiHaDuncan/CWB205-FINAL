import os

def getRecordPosition(num):
    ret = 0
    power = 0
    for c in num[::-1]:
        ret += alphabet.index(c) * pow(26,power)
        power += 1
    return ret


files = sorted(filter(lambda fileInDir: 'python_output' in fileInDir and 'processed' not in fileInDir, os.listdir('data4')), key=lambda fileName: int(fileName[13:]))
alphabet = "abcdefghijklmnopqrstuvwxyz"
compFile = open('output3_uniq','r')
#for i in range(int(files[0][13:])*500):
#    compFile.readline()
lastPosition = 0
for outputFile in files:
    inFile = open('data4/'+outputFile,'r')
    outFile = open('data4/processed_python_output' + outputFile[13:], 'a')

    for line in inFile:
        recordPosition = getRecordPosition(line.split(':')[0])

        while lastPosition < recordPosition-1:
            compFile.readline()
            lastPosition += 1

        lastPosition = recordPosition
        outFile.write(compFile.readline().rstrip() + ':' + line.split(':')[1])
