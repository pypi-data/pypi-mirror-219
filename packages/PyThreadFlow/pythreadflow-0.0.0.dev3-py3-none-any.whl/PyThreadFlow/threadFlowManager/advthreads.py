import threading as thread
import queue as cue
import warnings
import time as sun

class LegacyWarning(Warning):
    pass

def __deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(f"Call to deprecated function \"{func.__name__}\".", category=DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper

def __legacy(func):
    def wrapper(*args, **kwargs):
        warnings.warn(f"Call to legacy function \"{func.__name__}\".", category=LegacyWarning)
        return func(*args, **kwargs)
    return wrapper

def __deprecated_legacy(func):
    def wrapper(*args, **kwargs):
        warnings.warn(f"Call to deprecated legacy function \"{func.__name__}\".", category=Warning)
        return func(*args, **kwargs)
    return wrapper


@__deprecated_legacy
def x():
    return x

class basicEventThread():
    """## basicEventThread
    ### this is the most basic thread type, consisting of the following flags:

    #### `mainLoop`: the funciton that gets called every 0.5 seconds, it is required

    #### `openLoop`: the function that gets called before mainLoop, it is required

    #### `exitLoop`: the function that gets called when the exit function is called, it is required

    ### a basic example:
    
    ```python
    #...
    t = basicEventThread(network, initNetwork, exitNetwork, daemon=True, arguments = ("0.0.0.0", 8000))
    t.start() # start the threads
    time.sleep(40) # wait for the execution to finish
    t.stop() # calls the exitNetwork function, then exits the thread
    #...
    ```
    
    """
    def __init__(self, mainLoop:object, openLoop:object, exitloop:object, daemon:bool=False, arguments:tuple=(), delay=0.5):
        self.data = [mainLoop, openLoop, exitloop, daemon, arguments, delay]
        self.flags = [0 if arguments == () else 1, 1 if __name__ != "__main__" else 0]
    
    def __mloopy(this, argTuple, mloop, delay):
        while globals()['running'] == True:
            mloop(*argTuple)
            sun.sleep(delay)
        x = this.data[2]
        x()

    def start(self):
        globals()['running'] = True

        ithread = thread.Thread(target=self.data[1], daemon=self.data[3])
        self.ml = thread.Thread(target=self.__mloopy, daemon=self.data[3], args=(self.data[4], self.data[0], self.data[5]))
        ithread.start()
        ithread.join()
        self.ml.start()

    def stop(self):
        globals()['running'] = False
        self.ml.join()

    def instanceChecker(self):
        print(f"{self.data=}\n{self.flags=}")