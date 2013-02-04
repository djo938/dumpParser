#!/usr/bin/python

from datetime import datetime
import calendar
from logEvent import LogEvent
from nmeaEvent import *
from dumpEvent import *
from logException import LogParseException

#2013-01-18 20:09:23,044
def isFirstLine(line):
    return line != None and len(line) > 22 and line[4] == "-" and line[7] == "-" and line[10] == " " and line[13] == ":" and line[16] == ":" and line[19] == ","

def parseFile(File,Class,NewLogTest):
    f = open(File, 'r')
    
    objs = []
    obj = None
    for line in f:
        try:
            #is new log?
            if NewLogTest in line:
                obj = Class(File)
                objs.append(obj)
                continue
            else:
                if obj == None:
                    print "    WARNING, the first line of the file "+str(File)+" doesn't contain "+str(NewLogTest)
                    continue

            #is a first line ?
            if isFirstLine(line):
                timestamp = 0
                try:
                    #timestamp = calendar.timegm(.utctimetuple()) 
                    
                    #timestamp += float("0."+line[20:23])
                    timestamp = datetime(  int(line[0:4])  ,int(line[5:7]) ,  int(line[8:10]), int(line[11:13]) ,  int(line[14:16]) ,   int(line[17:19]), int(line[20:23])*1000 )
                except ValueError as ve:
                    print "    WARNING, failed to convert timestamp at line : "+line
                    continue
                ev = obj.newEvent(line[23:].strip(),timestamp)
                #print ev
                obj.eventList.append(ev)
                ev.log = obj
            else:
                if len(obj.eventList) == 0:
                    print "    WARNING, not a first line and no event in the list : {"+line+"}"
                    continue
            
                obj.eventList[-1].addLine(line)
        except LogParseException as lpe:
            print "    "+str(lpe)
            
    return objs

class Logstruct(object):
    def __init__(self, File):
        self.eventList = []
        self.File = File
            
    def newEvent(self,line, time):
        pass
    
class NmeaLog(Logstruct):
    fileCounter = {}

    def __init__(self,File):
        if File not in NmeaLog.fileCounter:
            NmeaLog.fileCounter[File] = 1
            self.fileIndice = 0
        else:
            self.fileIndice = NmeaLog.fileCounter[File]
            NmeaLog.fileCounter[File] += 1
    
        self.dateEvent = None
        
        self.NewPosition = []
        self.Position = []
        
        self.NewAltitude = []
        self.Altitude = []
        
        Logstruct.__init__(self,File)
        

    def newEvent(self,line, time):
        if line.startswith("altitude :"):
            ev = nmeaNewAltitudeEvent(time,line,True)
            self.NewAltitude.append(ev)
            self.Altitude.append(ev)
        elif line.startswith("altitude (not new) :"):
            ev = nmeaNewAltitudeEvent(time,line,False)
            self.Altitude.append(ev)
        elif line.startswith("position :"):
            ev = nmeaNewPositionEvent(time,line,True)
            self.NewPosition.append(ev)
            self.Position.append(ev)
        elif line.startswith("position (not new) :"):
            ev = nmeaNewPositionEvent(time,line,False)
            self.Position.append(ev)
        elif line.startswith("date "):
            ev = nmeaSetTimeEvent(time,line)
            
            if self.dateEvent != None:
                raise LogParseException("(NmeaLog) newEvent, two new date in file "+self.File)
                
            self.dateEvent = ev
            
        else:
            ev = LogEvent(time,"unknown event",line)
                        
        return ev
        
    def updateAllEventTime(self):
        if not isinstance(self.dateEvent,nmeaSetTimeEvent):
            print "    ERROR, no date event in file : "+str(self.File)+", index : "+str(self.fileIndice)
            return
        
        diff = self.dateEvent.timestamp - self.dateEvent.time
        #print "diff = ",diff
        
        for np in self.NewPosition:
            np.newTime = np.time + diff

def parseNmeaFile(File):
    return parseFile(File,NmeaLog,"nmead start")
        
class DumpLog(Logstruct):
    def __init__(self,File):
    
        self.dumpEvent = []
        self.dumps = []
    
        Logstruct.__init__(self,File)

    def newEvent(self,line, time):
        if line.startswith("card uid :"):
            ev = dumpNewDumpEvent(time,line)
            self.dumpEvent.append(ev)
        else:
            ev = LogEvent(time,"unknown event",line)
        
        return ev
        
def parseDumpLogFile(File):
    return parseFile(File,DumpLog,"server start")
        
