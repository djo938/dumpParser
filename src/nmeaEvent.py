#!/usr/bin/python

from logEvent import LogEvent
from datetime import datetime
import calendar
from utils import *
from logException import LogParseException

#date -s "25 JAN 2013 11:14:11"
class nmeaSetTimeEvent(LogEvent):
    def __init__(self,time,line):
        self.time = time
        
        line = line.strip()
        splittedSpace = line.split(" ")
        
        if len(splittedSpace) != 6 :
            raise LogParseException("(nmeaNewPositionEvent) __init__, invalid nmea datetime, space split",line)
            
        try:
            self.day =  int(splittedSpace[2][1:])
        except ValueError as va:
            raise LogParseException("(nmeaNewPositionEvent) __init__, invalid nmea day, int cast, "+str(va),line)
        
        self.month = 01 #TODO splittedSpace[3]
        
        try:
            self.year =  int(splittedSpace[4])
        except ValueError as va:
            raise LogParseException("(nmeaNewPositionEvent) __init__, invalid nmea year, int cast, "+str(va),line)
        
        splittedSpace[5] = splittedSpace[5].strip()
        splittedDoublePoint = splittedSpace[5].split(":")
        
        if len(splittedDoublePoint) != 3 :
            raise LogParseException("(nmeaNewPositionEvent) __init__, invalid nmea time, double point split",line)
        
        try:
            self.hour = int(splittedDoublePoint[0])
        except ValueError as va:
            raise LogParseException("(nmeaNewPositionEvent) __init__, invalid nmea hou, int cast, "+str(va),line)

        try:
            self.minute =  int(splittedDoublePoint[1])
        except ValueError as va:
            raise LogParseException("(nmeaNewPositionEvent) __init__, invalid nmea minute, int cast, "+str(va),line)

        try:
            self.second =  int(splittedDoublePoint[2][:-1])
        except ValueError as va:
            raise LogParseException("(nmeaNewPositionEvent) __init__, invalid nmea second, int cast, "+str(va),line)
        
        #self.timestamp = calendar.timegm(datetime(self.year,self.month,  self.day ,self.hour,self.minute,   self.second ).utctimetuple()) 
        self.timestamp = datetime(self.year,self.month,  self.day ,self.hour,self.minute,   self.second )
        
        LogEvent.__init__(self,time,"nmeaNewPositionEvent",line)
        
    def addLine(self,line):
        raise LogParseException("(nmeaNewPositionEvent) addLine, add line not allowed",line)
        
    def __str__(self):
        if self.newTime == None:
            return "(nmeaSetTimeEvent) at "+str(self.time)+" : "+str(self.day)+"/"+str(self.month)+"/"+str(self.year)+" "+str(self.hour)+":"+str(self.minute)+":"+str(self.second)
        else:
            return "(nmeaSetTimeEvent) at "+str(self.newTime)+" : "+str(self.day)+"/"+str(self.month)+"/"+str(self.year)+" "+str(self.hour)+":"+str(self.minute)+":"+str(self.second)
            
#position (not new) : 4516.2482N 00635.5607E, fix time : 101417
#position : 4516.2482N 00635.5607E, fix time : 101417
#position : 0000.0000N 00000.0000E
#position (not new) : 0000.0000N 00000.0000E
class nmeaNewPositionEvent(LogEvent):
    def __init__(self,time,line,New=False):
        self.time = time
        self.New = New
        
        self.longitude,self.latitude,self.fixtime = extractPosition(line)
        
        LogEvent.__init__(self,time,"nmeaNewPositionEvent",line)
        
    def addLine(self,line):
        raise LogParseException("(nmeaNewPositionEvent) addLine, add line not allowed",line)
        
    def __str__(self):
        if self.newTime == None:
            return "(nmeaNewPositionEvent) at "+str(self.time)+", longitude = "+str(self.longitude)+", latitude = "+str(self.latitude)
        else:
            return "(nmeaNewPositionEvent) at "+str(self.newTime)+", longitude = "+str(self.longitude)+", latitude = "+str(self.latitude)

#altitude (not new) : 2873.60009765625 M, fix time : 101418
#altitude : 2873.60009765625 M, fix time : 101418
#altitude (not new) : altitude : 0.0 M
#altitude : 0.0 M
class nmeaNewAltitudeEvent(LogEvent):
    def __init__(self,time,line,New=False):
        self.time = time
        self.New = New
        
        self.altitude,self.unit,self.fixtime = extractAltitude(line)
        
        LogEvent.__init__(self,time,"nmeaNewAltitudeEvent",line)
        
    def addLine(self,line):
        raise LogParseException("(nmeaNewAltitudeEvent) addLine, add line not allowed",line)
        
    def __str__(self):
        if self.newTime == None:
            return "(nmeaNewAltitudeEvent) at "+str(self.time)+", altitude = "+str(self.altitude)+" "+str(self.unit)
        else:
            return "(nmeaNewAltitudeEvent) at "+str(self.newTime)+", altitude = "+str(self.altitude)+" "+str(self.unit)
            
            
            
        
