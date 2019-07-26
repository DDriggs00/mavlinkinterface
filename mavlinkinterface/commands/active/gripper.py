from time import sleep  # for pressing button for a certain time
from mavlinkinterface.logger import getLogger


def gripperOpen(mcParams, sem, time):
    try:
        log = getLogger('gripper')

        if time > 2:
            time = 1.75

        log.trace('opening gripper for ' + str(time) + ' seconds')

        # use a bitwise or to avoid altering other buttons
        mcParams['b'] = mcParams['b'] | 1 << 10
        sleep(time)

    finally:
        mcParams['b'] = mcParams['b'] & (~(1 << 10))

        sem.release()


def gripperClose(mcParams, sem, time):
    try:
        log = getLogger('gripper')

        if time > 2:
            time = 1.75

        log.trace('opening gripper for ' + str(time) + ' seconds')

        # use a bitwise or to avoid altering other buttons
        mcParams['b'] = mcParams['b'] | 1 << 9
        sleep(time)

    finally:
        mcParams['b'] = mcParams['b'] & (~(1 << 9))

        sem.release()
