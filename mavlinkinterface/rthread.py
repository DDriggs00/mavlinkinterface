from threading import Thread

class RThread(Thread):    # https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
    '''A Thread subclass that returns the return value of the function upon using join()'''
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        try:
            if self._target is not None:
                self._return = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

    def join(self, *args):
        '''Returns the value of the threaded function'''
        Thread.join(self, *args)
        return self._return
