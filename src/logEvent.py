#!/usr/bin/python

class LogEvent(object):
    def __init__(self,time,name):
        self.time = time
        
        #TODO parse time
        
        self.name = name

    def addLine(self,line):
        pass