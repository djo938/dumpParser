#!/usr/bin/python
from utils import *
from datetime import time,datetime,date
from logException import LogParseException

def extractSimpleField(fieldName,line):
    splittedDoublePoint = line.split(":")
    if len(splittedDoublePoint) != 2:
        raise LogParseException("(FileDump) __init__, invalid "+fieldName+", double point split",line)
    
    return splittedDoublePoint[1].strip()

def parseHour(line):
    hindex = line.find("h")
    sindex = line.find("s")
    
    if hindex == -1 or sindex == -1:
        raise LogParseException("(FileDump) __init__, invalid hour, char h and s not found",line)
    
    #TODO check distance between h ans s
    
    hour    = line[:hindex]
    minute  = line[hindex+1:sindex]
    seconde = line[sindex+1:]
    
    try:
        return hour,minute,seconde,time(int(hour),int(minute),int(seconde))
    except ValueError as ve:
        raise LogParseException("(FileDump) __init__, invalid time, cast error : "+str(ve),line)

class FileDump(object):
    def __init__(self,File):
        self.File = File
        f = open(File, 'r')
        self.lines = []
        self.sectorValue = {}
        
        #get UID from file name
        #dump_E016246604C06B7A_6h2s6.txt
        underscoreSplit = File.split("_")
        
        if len(underscoreSplit) != 3 and len(underscoreSplit) != 6:
            raise LogParseException("(FileDump) __init__, invalid file name, undescrore split")
        
        self.UID = underscoreSplit[1]
        self.readType = None
        self.pixnn = None
        self.pixss = None
        self.cablecar = None
        self.skiSector = None
        self.cablecarPrecision = None
        self.cablecarPrecisionType = None
        #TODO store precision
        
        self.time = datetime.now().timetz()
        self.date = datetime.now().date()
        self.latitude = None
        self.longitude = None
        self.fixtime = None
        
        for line in f:
            if line.startswith("#") or line.startswith("//"):
                continue
            
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
                 
                self.hour,self.minute,self.seconde,self.time = parseHour(splittedDoublePoint[1])
                    
            elif line.startswith("Date : "):
                splitSpaceToken = line.split(" ")
                
                if len(splitSpaceToken) < 3:
                    raise LogParseException("(FileDump) __init__, invalid date line, space split",line)
                    
                splitSpaceToken[2] = splitSpaceToken[2].strip()
                
                if len(splitSpaceToken[2]) != 10 or splitSpaceToken[2][2] != "/" or splitSpaceToken[2][5] != "/":
                    raise LogParseException("(FileDump) __init__, invalid date line, length or slash position",line)
                
                try:
                    self.date = date(int(splitSpaceToken[2][6:]),int(splitSpaceToken[2][3:5]),int(splitSpaceToken[2][0:2]))
                except ValueError as ve:
                    raise LogParseException("(FileDump) __init__, invalid date, cast error : "+str(ve),line)
                    
            elif line.startswith("Degrees position : "):
                splitSpaceToken = line.split(" ")
                
                if len(splitSpaceToken) < 9:
                    raise LogParseException("(FileDump) __init__, invalid degrees position, space split",line)
                    
                try:
                    self.latitude = float(splitSpaceToken[3])
                except ValueError as ve:
                    raise LogParseException("(FileDump) __init__, invalid latitude, cast error : "+str(ve),line)
                    
                try:
                    self.longitude = float(splitSpaceToken[4][:-1])
                except ValueError as ve:
                    raise LogParseException("(FileDump) __init__, invalid longitude, cast error : "+str(ve),line)
                
                #BUG, can do that because the separator is double point in the file
                #self.fixtime = parseHour(splitSpaceToken[8])
                #self.fixtime = self.fixtime[3]
                self.fixtime = splitSpaceToken[8].strip()
                
            elif line.startswith("Cablecar : "):
                self.cablecar = extractSimpleField("cablecar",line)
            elif line.startswith("Cablecar area : "):
                self.skiSector = extractSimpleField("ski area",line)
            elif line.startswith("UID : "):
                pass #invalid uid in files
            elif line.startswith("PIX.SS : "):
                self.pixss = extractSimpleField("pix.SS",line)
            elif line.startswith("PIX.NN : "):
                self.pixnn = extractSimpleField("pix.NN",line)
            elif line.startswith("read type : "):
                self.readType = extractSimpleField("read type",line)
                
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
                
                #TODO save the locked or unlocked
                
            else:
                #TODO raise something ?
            
                self.lines.append(line)
            
            self.datetime = datetime.combine(self.date,self.time)
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
        if self.pixnn != None: 
            f.write("PIX.NN : "+self.pixnn+"\n")
            
        #write read type
        if self.readType != None: 
            f.write("read type : "+self.readType+"\n")
        
        if self.cablecar != None:
            f.write("Cablecar : "+self.cablecar+"\n")
        
        if self.skiSector != None:
            f.write("Cablecar area : "+self.skiSector+"\n")
        
        #write unknown data
        for line in self.lines:
            f.write(self.lines[i])
        
        #write data sector
        keys = sorted(self.sectorValue.keys())
        for key in keys:
            f.write("sector %0.2x: %0.8x\n"%(key,self.sectorValue[key]))        
            
            #TODO write the locked/unlocked    
            
        f.close()
        
