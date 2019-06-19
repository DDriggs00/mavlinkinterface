import logging
from datetime import date

def getLogger(name, fileName=None, doPrint=False, basic=False):
    if basic:
        logFormat = '%(asctime)s, %(message)s'
    else:
        logFormat = '%(asctime)s, %(name)8s, %(levelname)5s, %(message)s'

    if fileName:
        logFileName = fileName
    else:
        logFileName = ('log_' + str(date.today()) + '.log')

    logging.basicConfig(level=logging.DEBUG,
                        format=logFormat,
                        filename=logFileName,
                        filemode='w')
    if doPrint:
        consoleFormat = '%(message)s'
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(consoleFormat))
        logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)
