from typing import Callable, Any
import multiprocessing
from random import shuffle

class ParallelProcessing:
    def __init__(self, num_processes:int, initializer:Callable, initargs:tuple, task:Callable, job:list, do_result:Callable):
        self.pool = multiprocessing.Pool(processes=num_processes, initializer = initializer, initargs = initargs)
        self.initializer = initializer
        self.initargs = initargs
        self.task = task
        self.do_result = do_result
        self.job = job
        shuffle(self.job)
        self.completed = False

    def start(self):
        if self.completed:
            raise Exception('Job already done')
        for res in self.pool.imap_unordered(self.task, self.job):
            self.do_result(res)
        self.pool.close()
        self.pool.join()
        self.completed = True

    def startSingleProcess(self):
        self.initializer(*self.initargs)
        if self.completed:
            raise Exception('Job already done')
        for j in self.job:
            self.do_result(self.task(j))
        self.completed = True
