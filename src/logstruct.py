#!/usr/bin/python

from datetime import datetime
import calendar

#2013-01-18 20:09:23,044
def isFirstLine(line):
    return line != None and len(line) > 22 and line[4] == "-" and line[7] == "-" and line[10] == " " and line[13] == ":" and line[16] == ":" and line[19] == ","

class Logstruct(object):
    def __init__(self, File):
        self.eventList = []
        self.parseFile(File)
        
    def parseFile(self,File):
        f = open(File, 'r')
        for line in f:
            #is a first line ?
            if isFirstLine(line):
                timestamp = 0
                try:
                    timestamp = calendar.timegm(datetime(  int(line[0:4])  ,int(line[5:7]) ,  int(line[8:10]), int(line[11:13]) ,  int(line[14:16]) ,   int(line[17:19])  ).utcnow().utctimetuple()) 
                    
                    #TODO ca ne marche pas la somme, si les microseconde sont 9, ca fait xxx,9 ca devrait faire xxx,009
                    timestamp += float("0."+line[20:23])
                except ValueError as ve:
                    print "warning, failed to convert timestamp at line : "+line
                    continue
                
                self.eventList.append(self.newEvent(line[23:],timestamp))
            else:
                if len(self.eventList) == 0:
                    print "warning, not a first line and no event in the list : {"+line+"}"
                    continue
            
                #TODO self.eventList[-1].addLine(line)
            
    def newEvent(self,line, time):
        pass
        
class NmeaLog(Logstruct):
    def newEvent(self,line, time):
        print ""+str(time)+" : "+line
        
        pass #TODO 
        
class DumpLog(Logstruct):
    def newEvent(self,line, time):
        print ""+str(time)+" : "+line
        
        pass #TODO
