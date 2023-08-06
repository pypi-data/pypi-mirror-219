from time import time
import math

class MeanMetrics(object):
    def __init__(self):
        self.mean = {}
        self.variancek = {}
        self.count = {}

    def _addWeighted(self, name, value):
        self.count[name] += 1
        if name not in self.mean:
            self.mean[name] = value
            self.variancek[name] = 0.0
        else:
            #see https://math.stackexchange.com/a/116344
            m_next = ( (self.count[name] - 1) * self.mean[name] + value) / self.count[name]
            self.variancek[name] = self.variancek[name] + (value - self.mean[name])*(value - m_next)
            self.mean[name] = m_next

    def add(self, name, value):
        if name not in self.count:
            self.count[name] = 0
        self._addWeighted(name, value)
    
    def reset(self, name):
        if name not in self.count:
            return
        del self.count[name]
        del self.mean[name]
        del self.variancek[name]
    
    def toDict(self):
        return self.__dict__
    
    @classmethod
    def fromDict(cls, _dict):
        obj = MeanMetrics()
        obj.__dict__ = _dict
        return obj

    # def merge(self, metrics):
    #     for k in metrics.mean:
    #         if k not in self.mean:
    #             self.mean[k] = metrics.mean[k]
    #             self.variancek[k] = metrics.variancek[k]
    #         else:
    #             sc = self.count[k]
    #             mc = metrics.count[k]
    #             nc = sc + mc
    #             self.mean[k] = (sc*self.mean[k] + mc*metrics.mean[k]) / nc
    #             self.variancek[k] = (sc*self.variancek[k] + mc*metrics.variancek[k]) / nc

    #     for k in metrics.count:
    #         if k not in self.count:
    #             self.count[k] = metrics.count[k]
    #         else:
    #             self.count[k] += metrics.count[k]
    
    def __str__(self):
        string = ""
        for k,mean in self.mean.items():
            if self.count[k] <= 1.0:
                variance = 0.0
            else:
                variance = self.variancek[k] / (self.count[k] - 1.0)
            std = math.sqrt(variance)
            string += "\u001b[38;5;240m{}: n=\u001b[38;5;250m{:d} \u001b[38;5;240mµ=\u001b[38;5;250m{:.2f} \u001b[38;5;240m𝜎=\u001b[38;5;250m{:.4f}\n".format(k, self.count[k], mean, std)
        return string
