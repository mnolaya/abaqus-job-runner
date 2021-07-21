from time import time, localtime, asctime
"""
Custom stopwatch class for timing data extractions.
"""
# Stopwatch.
class stopwatch:

    def __init__(self):
        self.total_time = 0
        
    def start_clock(self):
        start = time()
        date = localtime()
        self.start = start
        self.date = asctime(date)

    def stop_clock(self):
        stop = time()
        self.stop = stop
        self.lap_clock()

    def lap_clock(self):
        lap = self.stop - self.start
        self.lap = lap
        self.sum_time()

    def sum_time(self):
        self.total_time = self.total_time + self.lap
