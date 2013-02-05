#!/usr/bin/python

from logEvent import LogEvent
from logException import LogParseException

#card uid : E0:16:24:66:04:C0:86:2C
class dumpNewDumpEvent(LogEvent):
    def __init__(self,time,line):
        
        line = line.strip()
        
        splittedSpace = line.split(" ")
        
        if(len(splittedSpace) != 4):
            raise LogParseException("(dumpNewDumpEvent) __init__, invalid line to dumpNewDumpEvent, space split",line)
            
        self.UID = splittedSpace[3]
        self.UID = self.UID.replace(":","")
        
        self.newTime = None
        
        LogEvent.__init__(self,time,"dumpNewDumpEvent",line)
        
    def addLine(self,line):
        raise LogParseException("(dumpNewDumpEvent) addLine, add line not allowed",line)
        
    def __str__(self):
        if self.newTime == None:
            return "dumpNewDumpEvent at "+str(self.time)+", uid = "+str(self.UID)
        else:
            return "dumpNewDumpEvent at "+str(self.newTime)+", uid = "+str(self.UID)
