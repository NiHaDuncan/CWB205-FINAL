from sys import argv, exit
import requests, json, os


def get_toxicity(text):

    localhost = 'http://localhost:5000/model/predict'
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(localhost, headers=headers, data=text)
    return response.json()

def initialSetup(data):
    if os.path.exists(data):
        outfile = open(data.split('.')[0] + '-toxicity.json', "r")
        res = None
        for i in json.load(outfile):
            res = i
        return res['repo']
    else:
        outfile = open(data.split('.')[0] + '-toxicity.json', "a")
        outfile.write("[\n")
        return "Yeah bruh, the file doesn't exist yet"

def read_json(data,lastRepo):

    json_file = open(data,)
    json_dict = json.load(json_file)

    outputfilename = data.split('.')[0] + "-toxicity.json"
    outfile = open(outputfilename, "a")

    print("Writing to", outputfilename, "...")

    index = 0

    repoFound = True if lastRepo == "Yeah bruh, the file doesn't exist yet" else False
    
    for i in json_dict:
        if not repoFound:
            if i['repo'] != lastRepo:
                continue
            else:
                repoFound = True
                continue
        response = get_toxicity(json.dumps(i))
        wrapped_response = {'repo': i['repo'], 'response' : response}
        json.dump(wrapped_response, outfile)
        outfile.write(",\n")
    
    outfile.write("\n]")

    outfile.close()
    print("Toxicity Classification written to ", outputfilename)


if __name__ == "__main__":
    print(len(argv))
    if len(argv) != 2:
        exit("usage: python3 "+argv[0]+" datafile")
    
    read_json(argv[1],initialSetup(argv[1]))
