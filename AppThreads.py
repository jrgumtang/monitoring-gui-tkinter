"""
Module: AppThreads Class
Description: Contains Application thread classes
            Class for serial read and logging
"""

from threading import Thread
from Utility import FileUtility, DataUtility

class SerialThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        FileUtility.createCSV()

    def run(self):
        DataUtility.getSerialData()
