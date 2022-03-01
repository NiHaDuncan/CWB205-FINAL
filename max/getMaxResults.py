import os, json

def buildLangDict(maxType):
    langDict = {}
    for dataFile in ([fileName for fileName in os.listdir('../twoweekdatapackage/') if 'processed' in fileName]):
        for l in (line for line in open('../twoweekdatapackage/'+dataFile,'r') if ':\n' not in line):
            for predictionType, predictionValue in maxType.items():
                if predictionValue['repo'] == l.split(':')[0]:
                    print(predictionType, predictionValue['repo'],predictionValue['original_text'],[(lang.split(',')[0],lang.split(',')[1].rstrip()) for lang in l.split(':')[1].split(';')])

def getMax():
    maxType = { 'toxic': {'value': 0, 'repo': '', 'original_text': ''},
                'severe_toxic': {'value': 0, 'repo': '', 'original_text': ''},
                'obscene': {'value': 0, 'repo': '', 'original_text': ''},
                'threat': {'value': 0, 'repo': '', 'original_text': ''},
                'insult': {'value': 0, 'repo': '', 'original_text': ''},
                'identity_hate': {'value': 0, 'repo': '', 'original_text': ''}}

    for pushEvent in (pushEvent for pushEvent in json.load(open('commentOutput3-toxicity.json','r')) if pushEvent['response']['status'] == 'ok'):
        for results in pushEvent['response']['results']:
            for predictionType, predictionValue in results['predictions'].items():
                if predictionValue > maxType[predictionType]['value']:
                    maxType[predictionType]['value'] = predictionValue
                    maxType[predictionType]['repo'] = pushEvent['repo']
                    maxType[predictionType]['original_text'] = results['original_text']
    return maxType

if __name__ == '__main__':
    langDict = buildLangDict(getMax())
