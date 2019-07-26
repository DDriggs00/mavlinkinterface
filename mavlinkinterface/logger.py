import logging                  # The logger
from datetime import date       # For naming log by date
from os.path import abspath     # For setting path based
from os.path import expanduser  # For setting path based
from os import makedirs         # For setting path based


def getLogger(name, fileName=None, doPrint=False, basic=False):
    # Logging levels
    # trace = 9
    # debug = 10
    # rdata = 15
    # info = 20
    # error = 30
    # warn = 40
    # critical = 50

    TRACE = 9
    RDATA = 15

    logging.addLevelName(TRACE, "TRACE")
    logging.addLevelName(RDATA, "RDATA")

    def trace(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'TRACE'.

        To log routine information, use the keyword argument exc_info with
        a true value, e.g.

        logger.trace("Houston, we have a %s", "thing to say, but it isn't really an issue", exc_info=1)
        """
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)

    def rdata(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'RDATA'.

        To log function return information, use the keyword argument exc_info with
        a true value, e.g.

        logger.rdata("Houston, we have a %s", "returned thing, no problems here", exc_info=1)
        """
        if self.isEnabledFor(RDATA):
            self._log(RDATA, msg, args, **kwargs)

    logging.Logger.trace = trace
    logging.Logger.rdata = rdata

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
    logging.basicConfig(level=TRACE,
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
