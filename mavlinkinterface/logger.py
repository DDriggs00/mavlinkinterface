import logging
from datetime import date

def get_logger(name):
    log_format = '%(asctime)s, %(name)8s, %(levelname)5s, %(message)s'
    logFileName = ('log_' + str(date.today()) + '.log')
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename=logFileName,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)
