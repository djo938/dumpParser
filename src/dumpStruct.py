#!/usr/bin/python
from utils import *
from datetime import time,datetime
from logException import LogParseException

class FileDump(object):
    def __init__(self,File):
        self.File = File
        f = open(File, 'r')
        self.lines = []
        self.sectorValue = {}
        
        #get UID from file name
        #dump_E016246604C06B7A_6h2s6.txt
        underscoreSplit = File.split("_")
        
        if len(underscoreSplit) != 3:
            raise LogParseException("(FileDump) __init__, invalid file name, undescrore split",line)
        
        self.UID = underscoreSplit[1]
        self.readType = None
        self.pixnn = None
        self.pixss = None
        self.cablecar = None
        self.time = datetime.now().timetz()
        self.date = datetime.now().date()
        
        for line in f:
            if line.startswith("Position :"): #PARSE NNMEA POSITION
                self.longitude,self.latitude,self.fixtime = extractPosition(line)
            elif line.startswith("Altitude : "): #PARSE NMEA ALTITUDE
                self.altitude,self.unit,self.altFixtime = extractAltitude(line)
            elif line.startswith("Heure : "): #PARSE TIME
                splittedDoublePoint = line.split(":")
                if len(splittedDoublePoint) != 2:
                    raise LogParseException("(FileDump) __init__, invalid hour, double point split",line)
                
                splittedDoublePoint[1] = splittedDoublePoint[1].strip()
                #6h2s6
                hindex = splittedDoublePoint[1].find("h")
                sindex = splittedDoublePoint[1].find("s")
                
                if hindex == -1 or sindex == -1:
                    raise LogParseException("(FileDump) __init__, invalid hour, char h and s not found",line)
                    
                self.hour    = splittedDoublePoint[1][:hindex]
                self.minute  = splittedDoublePoint[1][hindex+1:sindex]
                self.seconde = splittedDoublePoint[1][sindex+1:]
                
                
                try:
                    self.time = time(int(self.hour),int(self.minute),int(self.seconde))
                except ValueError as ve:
                    raise LogParseException("(FileDump) __init__, invalid time, cast error : "+str(ve),line)
            elif line.startswith("Date : "):
                pass #TODO
            elif line.startswith("Degrees position : "):
                pass #TODO
            elif line.startswith("Cablecar : "):
                splittedDoublePoint = line.split(":")
                if len(splittedDoublePoint) != 2:
                    raise LogParseException("(FileDump) __init__, invalid pix.SS, double point split",line)
                
                self.cablecar = splittedDoublePoint[1].strip()
            elif line.startswith("UID : "):
                pass #invalid uid in files
            elif line.startswith("PIX.SS : "):
                splittedDoublePoint = line.split(":")
                if len(splittedDoublePoint) != 2:
                    raise LogParseException("(FileDump) __init__, invalid pix.SS, double point split",line)
                
                self.pixss = splittedDoublePoint[1].strip()
            elif line.startswith("PIX.NN : "):
                splittedDoublePoint = line.split(":")
                if len(splittedDoublePoint) != 2:
                    raise LogParseException("(FileDump) __init__, invalid pix.NN, double point split",line)
                
                self.pixnn = splittedDoublePoint[1].strip()
            elif line.startswith("read type : "):
                splittedDoublePoint = line.split(":")
                if len(splittedDoublePoint) != 2:
                    raise LogParseException("(FileDump) __init__, invalid read type, double point split",line)
                
                self.readType = splittedDoublePoint[1].strip()
                
            elif line.startswith("sector "):
                #sector 1c: 2A:80:53:42 (Unlocked)
                splitSpaceToken = line.split(" ")
                
                if len(splitSpaceToken) < 3:
                    raise LogParseException("(FileDump) __init__, invalid sector line, space split",line)
                
                value = splitSpaceToken[2]
                value = value.replace(":","")
                
                key = splitSpaceToken[1]
                key = key.replace(":","")
                
                try:
                    self.sectorValue[int(key,16)]=int(value,16)
                except ValueError as va:
                    raise LogParseException("(FileDump) __init__, invalid sector key/value, cast error : "+str(va),line)
                
            else:
                #TODO raise something ?
            
                self.lines.append(line)
            
            self.datetime = datetime.combine(self.date,self.time)
            #TODO faire en sorte de ne plus avoir ces infos dans la classe, mais directement les lat/lon/datetime/etc
            #self.eventLog = None #link to the dump log event
            #self.nmeaEvent = None #link to the nmea log event
            self.cablecarInformation = None
                
    def __str__(self):
        return "(FileDump) at "+str(self.hour)+":"+str(self.minute)+":"+str(self.seconde)+" long="+str(self.longitude)+" lat="+str(self.latitude)+" fix="+str(self.fixtime)+", alt="+str(self.altitude)+str(self.unit)+" fix="+str(self.fixtime)
    
    def getSector(self, sectorIndex):
        return self.sectorValue[sectorIndex]
    
    def rewrite(self,directory="./"):
    
        f = open(directory+"dump_"+str(self.UID)+"_"+self.datetime.strftime("%d_%B_%Y_%Hh%Ms%S")+".txt", 'w')

        #write position
        if self.longitude != None and self.latitude != None and self.fixtime != None:
            f.write("Degrees position : "+str(self.latitude)+" "+str(self.longitude)+", fix time : "+str(self.fixtime)+"\n")
        
        #write altitude
        if self.altitude!= None and self.unit != None and self.altFixtime != None:
            f.write("Altitude : "+str(self.altitude)+" "+str(self.unit)+", fix time : "+str(self.altFixtime)+"\n")
        
        #write hour
        f.write("Heure : "+self.datetime.strftime("%Hh%Ms%S")+"\n")
        
        #write date
        f.write("Date : "+self.datetime.strftime("%d/%m/%Y")+"\n")
        
        #TODO mettre les milliseconds quelque part
        
        #write UID (hex)
        #TODO f.write("UID : %x\n"%self.UID)
            #prblm, uid is string
        
        #write UID (dec)
        f.write("UID : "+self.UID+"\n")
        
        #write PIX.SS
        if self.pixss != None: 
            f.write("PIX.SS : "+self.pixss+"\n")
            
        #write PIX.NN
        if self.pixss != None: 
            f.write("PIX.NN : "+self.pixnn+"\n")
            
        #write read type
        if self.readType != None: 
            f.write("read type : "+self.readType+"\n")
            
        #write unknown data
        for line in self.lines:
            f.write(self.lines[i])
        
        #write data sector
        keys = sorted(self.sectorValue.keys())
        for key in keys:
            f.write("sector %0.2x: %0.8x\n"%(key,self.sectorValue[key]))            
            
        f.close()
        
