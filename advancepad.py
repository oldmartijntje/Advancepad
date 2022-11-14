import json
import os

baseInterperator = {"store": "dataStore"}

def checkLoadSaveJson(location = '', data =''):
    if os.path.exists(f'{location}.json'):
        with open(f'{location}.json') as level_json_file:
            data = json.load(level_json_file)
            if type(data) != dict and type(data) != list:
                data = json.loads(data)
    else:
        with open(f'{location}.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)
    return data

def saveJson(location = '', data = ''):
    with open(f'{location}.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)

interperator = checkLoadSaveJson('interperator',baseInterperator)
if not os.path.isdir(interperator["store"]):
    os.mkdir(interperator["store"])