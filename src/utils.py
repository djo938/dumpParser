#!/usr/bin/python
from logException import LogParseException

def extractPosition(line):
    #TODO parse longitude,latitude to signed float

    line = line.strip()
    splittedDoublePoint = line.split(":")
    
    if len(splittedDoublePoint) != 3 and len(splittedDoublePoint) != 2:
        raise LogParseException("(utils.py) extractPosition, invalid nmea Position, double point split",line)
        
    #latitude-longitude
    splittedDoublePoint[1] = splittedDoublePoint[1].strip()
    splittedSpace = splittedDoublePoint[1].split(" ")
    
    if len(splittedDoublePoint) != 2:
        if len(splittedSpace) != 4:
            raise LogParseException("(utils.py) extractPosition, invalid nmea Position, space split (1)",line)
            
        #self.longitude = splittedSpace[0]
        #self.latitude  = splittedSpace[1][:-1]
        
        #fix time
        splittedDoublePoint[2] = splittedDoublePoint[2].strip()
        if len(splittedDoublePoint[2]) != 6:
            raise LogParseException("(utils.py) extractPosition, invalid nmea Position, fix time length",line)
            
        #self.fixtime = splittedDoublePoint[2]
        #self.hour    = line[-6:-4]
        #self.minute  = line[-4:-2]
        #self.seconds = line[-2:][:2]
        
        return splittedSpace[0],splittedSpace[1][:-1],splittedDoublePoint[2]
    else:
        if splittedDoublePoint[1] == "unknown":
            return None,None,None
    
        if len(splittedSpace) != 2:
            raise LogParseException("(utils.py) extractPosition, invalid nmea Position, space split (2)",line)
            
        #self.longitude = splittedSpace[0]
        #self.latitude  = splittedSpace[1]
        #self.fixtime = None
        
        return splittedSpace[0],splittedSpace[1],None
        
def extractAltitude(line):
    line = line.strip()
    splittedDoublePoint = line.split(":")
    
    if len(splittedDoublePoint) != 3 and len(splittedDoublePoint) != 2:
        raise LogParseException("(utils.py) extractAltitude, invalid nmea altitude, double point split",line)
    
    #altitude
    splittedDoublePoint[1] = splittedDoublePoint[1].strip()
    splittedSpace = splittedDoublePoint[1].split(" ")
    
    if len(splittedDoublePoint) != 2:
        if len(splittedSpace) != 4:
            raise LogParseException("(utils.py) extractAltitude, invalid nmea altitude, space split (1)",line)
    
        altitude = None
        try:
            altitude = float(splittedSpace[0])
        except ValueError as va:
            raise LogParseException("(utils.py) extractAltitude, invalid nmea altitude, float cast (1)",line)
        
        #units
        #self.unit = splittedSpace[1][:-1]
    
        #fix time
        splittedDoublePoint[2] = splittedDoublePoint[2].strip()
        if len(splittedDoublePoint[2]) != 6:
            raise LogParseException("(utils.py) extractAltitude, invalid nmea altitude, fix time length",line)
            
        #self.fixtime = splittedDoublePoint[2]
        
        return altitude, splittedSpace[1][:-1], splittedDoublePoint[2]
    else:
        if splittedDoublePoint[1] == "unknown":
            return None,None,None
    
        if len(splittedSpace) != 2:
            raise LogParseException("(utils.py) extractAltitude, invalid nmea altitude, space split (2)",line)
            
        altitude = None
        try:
            altitude = float(splittedSpace[0])
        except ValueError as va:
            raise LogParseException("(utils.py) extractAltitude, invalid nmea altitude, float cast (2)",line)
        
        #units
        #self.unit = splittedSpace[1]
        #self.fixtime = None
        
        return altitude, splittedSpace[1], None
        

