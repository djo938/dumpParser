#!/usr/bin/python

class LogParseException(Exception):
    def __init__(self,message,line = None):
        self.message = message
        self.line = line
        
    def __str__(self):
        if self.line == None:
            return str(self.message)
        else:
            return str(self.message)+" : \""+self.line+"\""
