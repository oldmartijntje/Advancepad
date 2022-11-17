import json
import os
import datetime
import random


# logging types:
# none
# all
# error
# modify
# warning
# deleteAfter

interperatorFile = 'interperator'
fileExtension = '.json'
interperatorFileExtension = fileExtension
maxPathLength = 10
baseInterperator = {"storeData": ["dataStore"], "logging": {"where": ["logFiles"], "type": ["all"]},
    "context": {"idNumber":0}, "library":"libraryContext", "extension": ".json"}
baseLibContext = {"names": {}}
logFile = ''
basePath = ''
interperator = {}
libContext = {}

def checkLoadSaveJson(location = '', data =''):
    if os.path.exists(f'{location}{fileExtension}'):
        with open(f'{location}{fileExtension}') as level_json_file:
            data = json.load(level_json_file)
            if type(data) != dict and type(data) != list:
                data = json.loads(data)
    else:
        with open(f'{location}{fileExtension}', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        checkLogging(f'made file: {location}{fileExtension}', 'modify')
    return data

def saveFile(location = '', data = ''):
    if location != '' and data != '':
        checkLogging(f"savefile: {location}", 'modify')
        if location == interperatorFile:
            with open(f'{location}{interperatorFileExtension}', 'w') as outfile:
                json.dump(data, outfile, indent=4)
        else:
            with open(f'{location}{fileExtension}', 'w') as outfile:
                json.dump(data, outfile, indent=4)

def logging(itemToLog: str = '', type = ''):
    if logFile != '':
        log = open(f'{logFile}', "a+")
        log.write(f'{type}{itemToLog}\n\n')
        log.close() 

def checkLogging(logMessage: str = '', typeOfLog: str = 'info'):
    if len(interperator) > 0 and logFile != '':
        if logMessage != '' and "none" not in interperator["logging"]["type"]:
            if typeOfLog == 'info' and 'all' in interperator["logging"]["type"]:
                logging(logMessage)
            elif typeOfLog == 'warning' and ('all' in interperator["logging"]["type"] or 'warning' in interperator["logging"]["type"]):
                logging(logMessage, '> Warning: ')
            elif typeOfLog == 'error' and ('all' in interperator["logging"]["type"] or 'error' in interperator["logging"]["type"]):
                logging(logMessage, '> Error: ')
            elif typeOfLog == 'modify' and ('all' in interperator["logging"]["type"] or 'modify' in interperator["logging"]["type"]):
                logging(logMessage, 'fileChange: ')
            elif typeOfLog in interperator["logging"]["type"] or 'all' in interperator["logging"]["type"]:
                logging(logMessage)


def checkMakeFolderPath(givenPath: list = []):
    if len(givenPath) > maxPathLength:
        raise RecursionError(f"path exeeds the maximum amount of levels: {givenPath} whilst maximum is a level of {maxPathLength}")
    currentPath = ''
    for pathPart in givenPath:
        if "/" in pathPart or "\\" in pathPart:
            raise NameError(f"you can't put a '/' or '\\' in the path, the program does that automativcally.\n{pathPart} in {givenPath} after {currentPath}")
        if currentPath != '':
            currentPath = f"{currentPath}/{pathPart}"
        else:
            currentPath = pathPart
        if not os.path.isdir(currentPath):
            if logFile != '':
                checkLogging(f"os.mkdir({currentPath}) = currentPath", 'modify')
            os.mkdir(currentPath)
    return currentPath

def exitCode():
    saveFile(interperator["library"],libContext)
    saveFile(interperatorFile,interperator)
    log = open(f'{logFile}', "r")
    text = log.read()
    log.close()
    if text == '' or "deleteAfter" in interperator["logging"]["type"]:
        os.remove(f'{logFile}')

def createFile(name):
    def stringToAscii(seedString:str): #turns everything into ther ASCII value
        seedList = []
        for x in seedString:
            seedList.append(ord(x))#change every character into its ASCII value
        seedString = ''.join([str(elem) for elem in seedList])#add list together into string
        seed = int(seedString)
        return seed
    
    fileKey = stringToAscii(f"{fileExtension}{datetime.datetime.now().strftime('%d%m%Y%H%M%S')}{name}{random.randint(0,10)}")
    checkLogging(f"making: {fileKey}", 'modify')
    if name in libContext["names"]:
        libContext["names"][name].append(f'{fileKey}{fileExtension}')
    else:
        libContext["names"][name] = [f'{fileKey}{fileExtension}']
    file = {"title": name, "id": fileKey, "fileExtension": fileExtension, "contents": {"dict": {"defaultBox": "Hello World!"}, "list": ["defaultBox"]}}
    checkLoadSaveJson(f"{basePath}/{fileKey}", file)


interperator = checkLoadSaveJson(interperatorFile,baseInterperator)

if not "extension" in interperator:
    interperator["extension"] = baseInterperator["extension"]
    checkLogging(f"interperator[\"extension\"] was not a thing, so we made it ```{interperator['extension']}```", 'warning')
fileExtension = interperator["extension"]
if not "logging" in interperator:
    interperator["logging"] = baseInterperator["logging"]
    checkLogging(f"interperator[\"logging\"] was not a thing, so we made it ```{interperator['logging']}```", 'warning')
if not "where" in interperator["logging"]:
    interperator["logging"]["where"] = baseInterperator["logging"]["where"]
    checkLogging(f"interperator[\"logging\"][\"where\"] was not a thing, so we made it ```{interperator['logging']['where']}```", 'warning')
if not "type" in interperator["logging"]:
    interperator["logging"]["type"] = baseInterperator["logging"]["type"]
    checkLogging(f"interperator[\"logging\"][\"type\"] was not a thing, so we made it ```{interperator['logging']['type']}```", 'warning')
if "none" not in baseInterperator["logging"]["type"]:
    logFile = checkMakeFolderPath(interperator["logging"]["where"])
    logFile = f"{logFile}/log{datetime.datetime.now().strftime('%d_%m_%Y-%H_%M_%S')}.md"
    log = open(logFile, "w")
    log.close()  
if not "storeData" in interperator:
    interperator["storeData"] = baseInterperator["storeData"]
    checkLogging(f"interperator[\"storeData\"] was not a thing, so we made it ```{interperator['storeData']}```", 'warning')
basePath = checkMakeFolderPath(interperator["storeData"])
if not "context" in interperator:
    interperator["context"] = baseInterperator["context"]
    checkLogging(f"interperator[\"context\"] was not a thing, so we made it ```{interperator['context']}```", 'warning')
if not "library" in interperator:
    interperator["library"] = baseInterperator["library"]
    checkLogging(f"interperator[\"storeData\"] was not a thing, so we made it ```\"{interperator['library']}\"```", 'warning')
libContext = checkLoadSaveJson(interperator["library"],baseLibContext)




createFile('henk')



# os.remove(f'interperator.json')

exitCode()
