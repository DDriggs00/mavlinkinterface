import logging                  # The logger
from datetime import date       # For naming log by date
from os.path import abspath     # For setting path based
from os.path import expanduser  # For setting path based
from os import makedirs         # For setting path based


def getLogger(name, fileName=None, doPrint=False, basic=False):
    if basic:
        logFormat = '%(asctime)s, %(message)s'
    else:
        logFormat = '%(asctime)s, %(name)8s, %(levelname)5s, %(message)s'

    if fileName:
        logPath = abspath(expanduser("~/logs/mavlinkInterface/"))
    else:
        fileName = ('log_' + str(date.today()) + '.log')
        logPath = abspath(expanduser("~/logs/mavlinkInterface/"))
    makedirs(logPath, exist_ok=True)    # Make the directory path if not exists
    logging.basicConfig(level=logging.DEBUG,
                        format=logFormat,
                        filename=logPath + '/' + fileName,
                        filemode='a+')
    if doPrint:
        consoleFormat = '%(message)s'
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(consoleFormat))
        logging.getLogger(name).addHandler(console)
        logging.getLogger(name).optionxform = str
    return logging.getLogger(name)
