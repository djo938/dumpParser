#!/usr/bin/python
from utils import *
from datetime import time

class FileDump(object):
    def __init__(self,File):
        self.File = File
        f = open(File, 'r')
        indice = 0
        self.lines = []
        
        #get UID from file name
        #dump_E016246604C06B7A_6h2s6.txt
        underscoreSplit = File.split("_")
        if len(underscoreSplit) != 3:
            print "(FileDump) WARNING, invalid file name, undescrore split : "+str(line)
            self.hour = None 
            self.minute = None 
            self.seconds = None
        
        self.UID = underscoreSplit[1]
        
        for line in f:
            if indice == 0: #position
                self.longitude,self.latitude,self.fixtime = extractPosition(line)
            elif indice == 1: #altitude
                self.altitude,self.unit,self.fixtime = extractAltitude(line)
            elif indice == 2: #Heure : 6h2s6
                splittedDoublePoint = line.split(":")
                if len(splittedDoublePoint) != 2:
                    print "(FileDump) WARNING, invalid hour, double point split : "+str(line)
                    self.hour = None 
                    self.minute = None 
                    self.seconds = None
                    indice += 1
                    self.lines.append(line)
                    continue
                
                splittedDoublePoint[1] = splittedDoublePoint[1].strip()
                #6h2s6
                hindex = splittedDoublePoint[1].find("h")
                sindex = splittedDoublePoint[1].find("s")
                
                if hindex == -1 or sindex == -1:
                    print "(FileDump) WARNING, invalid hour, double point split : "+str(line)
                    self.hour = None 
                    self.minute = None 
                    self.seconds = None
                    indice += 1
                    self.lines.append(line)
                    continue
                    
                self.hour    = splittedDoublePoint[1][:hindex]
                self.minute  = splittedDoublePoint[1][hindex+1:sindex]
                self.seconde = splittedDoublePoint[1][sindex+1:]
                
                
                try:
                    self.time = time(int(self.hour),int(self.minute),int(self.seconde))
                except ValueError as ve:
                    self.time = None
                
            indice += 1
            self.lines.append(line)
            
                
    def __str__(self):
        return "(FileDump) at "+str(self.hour)+":"+str(self.minute)+":"+str(self.seconde)+" long="+str(self.longitude)+" lat="+str(self.latitude)+" fix="+str(self.fixtime)+", alt="+str(self.altitude)+str(self.unit)+" fix="+str(self.fixtime)
        
    def rewrite(self,directory="./"):
        f = open(directory+"dump_"+self.eventLog.newTime.strftime("%d_%A_%B_%Y_%Hh%Ms%S")+".txt", 'w')

        for i in range(0,len(self.lines)):
            if i == 2:
                f.write("Heure : "+self.eventLog.newTime.strftime("%Hh%Ms%S")+"\n")
                continue
        
            f.write(self.lines[i]+"\n")
            
            
        f.close()
        
