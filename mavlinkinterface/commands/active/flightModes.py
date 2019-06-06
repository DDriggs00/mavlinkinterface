# from threading import Semaphore

def setFlightMode(ml, sem, mode):
    # set flight mode
    print("Setting Flight Mode to " + str(mode))
    sem.release()
    return
