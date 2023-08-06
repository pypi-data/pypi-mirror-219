from time import time

class TimeMetrics(object):
    def __init__(self):
        self.timestamp = {}
        self.duration = {}
        self.count = {}

    def _addWeighted(self, name, duration):
        self.count[name] += 1
        if name not in self.duration:
            self.duration[name] = duration
        else:
            self.duration[name] = ( (self.count[name] - 1) * self.duration[name] + duration) / self.count[name]

    def start(self, name):
        self.timestamp[name] = time()*1000.0
        if name not in self.count:
            self.count[name] = 1
        else:
            self.count[name] += 1
        return self

    def end(self, name):
        self._addWeighted(name, time()*1000.0 - self.timestamp[name])
        return self
    
    def toDict(self):
        return self.__dict__

    def reset(self, name):
        if name not in self.count:
            return self
        del self.count[name]
        del self.duration[name]
        del self.timestamp[name]
        return self
    
    @classmethod
    def fromDict(cls, _dict):
        obj = TimeMetrics()
        obj.__dict__ = _dict
        return obj

    def merge(self, metrics):
        for k in metrics.duration:
            if k not in self.duration:
                self.duration[k] = metrics.duration[k]
            else:
                sc = self.count[k]
                mc = metrics.count[k]
                nc = sc + mc
                self.duration[k] = (sc*self.duration[k] + mc*metrics.duration[k]) / nc

        for k in metrics.count:
            if k not in self.count:
                self.count[k] = metrics.count[k]
            else:
                self.count[k] += metrics.count[k]
        return self
    
    def __str__(self):
        string = ""
        for k,v in self.duration.items():
            string += "\u001b[38;5;240m{}: \u001b[38;5;250m{:.2f}ms\t".format(k, v)
        return string
