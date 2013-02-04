#!/usr/bin/python

class LogEvent(object):
    def __init__(self,time,name,line):
        self.time = time
        self.name = name
        self.lines = [line]
        
        #self.addLine(line)
        self.newTime = None

    def addLine(self,line):
        self.lines.append(line)
        
    def __str__(self):
        return "("+str(self.name)+") at "+str(self.time)+" : "+str(self.lines)
        
    def __repr__(self):
        return str(self)
        
    def __lt__(self, other):
        if other == None:
            return False
    
        if self.newTime != None and other.newTime != None:
            return self.newTime < other.newTime
        else:
            return self.time < other.time
            
    def __gt__(self, other):
        if other == None:
            return False
    
        if self.newTime != None and other.newTime != None:
            return self.newTime > other.newTime
        else:
            return self.time > other.time
            
    def __eq__(self, other):
        if other == None:
            return False
    
        if self.newTime != None and other.newTime != None:
            return self.newTime == other.newTime
        else:
            return self.time == other.time
            
    def __le__(self, other):
        if other == None:
            return False
    
        if self.newTime != None and other.newTime != None:
            return self.newTime <= other.newTime
        else:
            return self.time <= other.time
            
    def __ge__(self, other):
        if other == None:
            return False
    
        if self.newTime != None and other.newTime != None:
            return self.newTime >= other.newTime
        else:
            return self.time >= other.time
            
    def __ne__(self, other):
        if other == None:
            return False
    
        if self.newTime != None and other.newTime != None:
            return self.newTime != other.newTime
        else:
            return self.time != other.time
