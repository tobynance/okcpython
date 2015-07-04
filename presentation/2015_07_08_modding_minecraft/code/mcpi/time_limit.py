import sys, threading, ctypes

#######################################################################
class TimeoutError(Exception): pass


#######################################################################
class InterruptableThread(threading.Thread):
    ###################################################################
    @classmethod
    def _async_raise(cls, tid, excobj):
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(excobj))
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    ###################################################################
    def raise_exc(self, excobj):
        assert self.isAlive(), "thread must be started"
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._async_raise(tid, excobj)
                return

    ###################################################################
    def terminate(self):
        self.raise_exc(SystemExit)


#######################################################################
def time_limit(timeout):
    ###################################################################
    def internal(function):
        def internal2(*args, **kw):
            class Calculator(InterruptableThread):
                def __init__(self):
                    InterruptableThread.__init__(self)
                    self.result = None
                    self.error = None
                    self.daemon = True

                def run(self):
                    try:
                        self.result = function(*args, **kw)
                    except:
                        self.error = sys.exc_info()[0]

            c = Calculator()
            c.start()
            c.join(timeout)
            if c.isAlive():
                c.terminate()
                raise TimeoutError
            if c.error:
                raise c.error
            return c.result
        return internal2
    return internal
