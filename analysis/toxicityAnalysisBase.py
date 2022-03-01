import os, json

def buildLangDict(maxType):
    for dataFile in ([fileName for fileName in os.listdir('../twoweekdatapackage/') if 'processed' in fileName]):
        for l in (line for line in open('../twoweekdatapackage/'+dataFile,'r') if ':\n' not in line):
            for predictionType, predictionValue in maxType.items():
                for entry in predictionValue['entries']:
                    if l.split(':')[0] == entry['repo']:
                        entry['languages'] = [(lang.split(',')[0],lang.split(',')[1].rstrip()) for lang in l.split(':')[1].split(';')]
    return maxType

def addAndSort(predictionType, newEntry):
    if len(predictionType['entries']) == topN:
        predictionType['entries'][0] = newEntry
        predictionType['minValue'] = min(value['value'] for value in predictionType['entries'])
    else:
        predictionType['entries'].append(newEntry)

    predictionType['entries'] = sorted(predictionType['entries'], key=lambda l: l['value'])
    return predictionType

def getMax():
    maxType = { 'toxic': {'minValue': 0, 'entries': []},
                'severe_toxic': {'minValue': 0, 'entries': []},
                'obscene': {'minValue': 0, 'entries': []},
                'threat': {'minValue': 0, 'entries': []},
                'insult': {'minValue': 0, 'entries': []},
                'identity_hate': {'minValue': 0, 'entries': []}}

    for pushEvent in (pushEvent for pushEvent in json.load(open('commentOutput-toxicity.json','r')) if pushEvent['response']['status'] == 'ok'):
        for results in pushEvent['response']['results']:
            for predictionType, predictionValue in results['predictions'].items():
                if predictionValue > maxType[predictionType]['minValue']:
                    maxType[predictionType] = addAndSort(maxType[predictionType], {'repo': pushEvent['repo'], 'original_text': results['original_text'], 'value': predictionValue})
                    continue
    return maxType

if __name__ == '__main__':
    topN = 10
    maxType = buildLangDict(getMax())
    for k,v in maxType.items():
        print(k,v)
