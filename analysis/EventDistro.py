import json


def runAnalysis():
    eventID = "PushEvent"

    res = dict()

    for line in open("data/2021-01-01-0.json"):
        data = json.loads(line)
        if data['type'] in res:
            res[data['type']] += 1
        else:
            res[data['type']] = 1

    nonEvents = 0
    events = 0

    for key in res:
        print(key, ", ", res[key])
        if key == eventID:
            events = res[key]
        else:
            nonEvents += res[key]
    return [events, nonEvents]


if __name__ == "__main__":
    fileBase = "data/2021-01-01-"
    nonEvents = 0
    events = 0
    for i in range(10):
        #newRes = runAnalysis((fileBase + str(i) + '.json'), res)
        res = runAnalysis((fileBase + str(i) + '.json'))
        events += res[0]
        nonEvents += res[1]
        #res.update(newRes)


    print("\n\nNumber of PushEvents: ", events, "\nNumber of non-PushEvents: ", nonEvents)
    print("PushEvent/Other: ", events/nonEvents)
