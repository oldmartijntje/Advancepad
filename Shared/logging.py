class Logger:
    def __init__(self, logfilePath = 'logFiles/', logfileName = 'log-', logFileExtention = 'log', defaultLoggingLevel = '', deleteWhenDone = False, addDatetimeToName = True, datetimeFormat = '%d_%m_%Y-%H_%M_%S', insideLogfileDatetimeFormat = '%d/%m/%Y %H:%M:%S', formatting = '| {type} | {time} | {message}'):	
        self.pathing = logfilePath
        self.name = logfileName
        self.deleteWhenDone = deleteWhenDone
        if addDatetimeToName:
            import datetime
            logfileName = '{}{}.{}'.format(logfileName, datetime.datetime.now().strftime(datetimeFormat), logFileExtention)
        self.insideLogfileDatetimeFormat = insideLogfileDatetimeFormat
        self.formatting = formatting
        self.defaultLoggingLevel = defaultLoggingLevel
        self.checkExistance()

    def checkExistance(self):
        import os
        if not os.path.exists(self.pathing):
            os.makedirs(self.pathing)
        if not os.path.exists(self.pathing + self.name):
            open(self.pathing + self.name, 'w').close()

    def log(self, message, type = 'DEFAULT'):
        import datetime
        if type == 'DEFAULT':
            type = self.defaultLoggingLevel
        with open(self.pathing + self.name, 'a') as file:
            file.write(self.formatting.format(type = type, time = datetime.datetime.now().strftime(self.insideLogfileDatetimeFormat), message = message))



