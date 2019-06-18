import logging
from datetime import date

def getLogger(name, fileName=None):
    logFormat = '%(asctime)s, %(name)8s, %(levelname)5s, %(message)s'
    consoleFormat = '%(message)s'
    if not fileName:
        logFileName = ('log_' + str(date.today()) + '.log')
    else:
        logFileName = fileName
    logging.basicConfig(level=logging.DEBUG,
                        format=logFormat,
                        filename=logFileName,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(consoleFormat))
    logging.getLogger(name).addHandler(console)
    logging.getLogger(name).debug("Logger Successfully Initiated")
    return logging.getLogger(name)
