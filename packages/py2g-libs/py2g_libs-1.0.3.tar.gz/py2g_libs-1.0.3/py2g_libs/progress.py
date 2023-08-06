import shutil
from time import time
import math
from datetime import timedelta


REFETCH_TERMINAL_SIZE = 10

class ProgressMetrics(object):
    def __init__(self):
        self.count = {}
        self.limit = {}
        self.timestamps = {}

        self.refetchCount = 0

        self._printed = 0

    def _fetchTerminalSize(self):
        if self.refetchCount == 0:
            self.terminal_size = shutil.get_terminal_size((80, 20))
        self.refetchCount = (self.refetchCount + 1) % REFETCH_TERMINAL_SIZE
        return self.terminal_size
    
    def clearConsole(self):
        print("\033[2J")

    def start(self, numberOfSteps, name='total'):
        self.limit[name] = numberOfSteps
        self.count[name] = 0
        self.timestamps[name] = time()

    def restart(self, name='total'):
        self.count[name] = 0
        self.timestamps[name] = time()

    def estimate(self, name='total', currentTime=time()):
        if name not in self.count:
            return 0.0
        took = currentTime - self.timestamps[name]
        totalProgress = self.count[name]/self.limit[name]
        if totalProgress == 0.0:
            return 0.0
        return (1.0-totalProgress) * took / totalProgress

    def step(self, name='total'):
        self.count[name] += 1
    
    def toConsole(self, main='total', other=[], every=1):
        self._printed = (self._printed + 1) % every
        if self._printed != 0:
            return

        self.clearConsole()
        width, _ = self._fetchTerminalSize()
        for o in other:
            classname = o.__class__.__name__
            print("{}\u001b[38;5;240m{}".format(" "*(width//2 - len(classname)//2), classname))
            print(str(o))
            print("_"*width)
            print()

        classname = self.__class__.__name__
        print("{}\u001b[38;5;240m{}".format(" "*(width//2 - len(classname)//2), classname))

        if main in self.count:
            width -= 3
            totalProgress = self.count[main]/self.limit[main]
            eqs = int(width*totalProgress)
            print("\u001b[38;5;240m[\u001b[38;5;250m{}\u001b[38;5;240m>{}]".format('='*eqs, ' '*(width-eqs)))
        print(str(self))

    def _getPercent(self, name):
        if name not in self.count:
            return None
        return 100.0 * self.count[name]/self.limit[name]

    def __str__(self):
        string = ""
        currentTime = time()
        for k,v in self.count.items():
            string += "\u001b[38;5;240m{}: \u001b[38;5;250m{}/{} {:.2f}% ({})\t".format(k, v, self.limit[k], self._getPercent(k), str(timedelta(seconds=self.estimate(name=k, currentTime=currentTime))))
        return string

if __name__ == '__main__':
    from time import sleep
    testPs = ProgressMetrics()
    testPs.start(100)
    testPs.start(200, name='current')
    for i in range(0,100):
        testPs.step()
        testPs.step('current')
        testPs.toConsole()
        sleep(0.05)
