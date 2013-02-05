#!/usr/bin/python
from logException import LogParseException
from datetime import time

def extractPosition(line):

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
        
        latitudeString = splittedSpace[0]
        longitudeString = splittedSpace[1][:-1]
        fixtimeString = splittedDoublePoint[2]
    else:
        if splittedDoublePoint[1] == "unknown":
            return None,None,None
    
        if len(splittedSpace) != 2:
            raise LogParseException("(utils.py) extractPosition, invalid nmea Position, space split (2)",line)
            
        #self.longitude = splittedSpace[0]
        #self.latitude  = splittedSpace[1]
        #self.fixtime = None
        
        latitudeString = splittedSpace[0]
        longitudeString = splittedSpace[1]
        fixtimeString = None
    
    longitudeString = longitudeString.strip()
    latitudeString = latitudeString.strip()
    
    #print "<"+longitudeString+"><"+latitudeString+"><"+fixtimeString+">"
    #TODO check string length
    
    longitudeDirection = longitudeString[-1:]
    longitudeString = longitudeString[:-1]
    
    latitudeDirection = latitudeString[-1:]
    latitudeString = latitudeString[:-1]
    
    longitudeStringDotIndex = longitudeString.index(".")
    latitudeStringDotIndex = latitudeString.index(".")
    
    longitudeStringDotIndex -= 2 #on se decale pour avoir l'heure
    latitudeStringDotIndex -= 2 #on se decale pour avoir l'heure
    
    if longitudeStringDotIndex <= 0: #TODO make more test
        raise LogParseException("(utils.py) extractPosition, invalid nmea Position, dot longitude is not on a correct place",line)
        
    if latitudeStringDotIndex <= 0: #TODO make more test
        raise LogParseException("(utils.py) extractPosition, invalid nmea Position, dot latitude is not on a correct place",line)
    
    longitudeDegree = 0.0
    try:
        longitudeDegree = float(longitudeString[0:longitudeStringDotIndex])
        hour = float(longitudeString[longitudeStringDotIndex:])
        longitudeDegree += (hour / 60.0)
    except ValueError as ve:
        pass
        
    if longitudeDirection == "W":
        longitudeDegree *= -1
    elif longitudeDirection != "E":
        raise LogParseException("(utils.py) extractPosition, invalid nmea Position, invalid longitude direction",line)
        
    latitudeDegree = 0.0
    try:
        latitudeDegree = float(latitudeString[0:latitudeStringDotIndex])
        hour = float(latitudeString[latitudeStringDotIndex:])
        latitudeDegree += (hour / 60.0)
    except ValueError as ve:
        pass
    
    if latitudeDirection == "S":
        latitudeDegree *= -1
    elif latitudeDirection != "N":
        raise LogParseException("(utils.py) extractPosition, invalid nmea Position, invalid latitude direction",line)
    
    timedFixTime = None
    if fixtimeString != None:
        fixtimeString  =fixtimeString.strip()
        if len(fixtimeString) != 6:
            raise LogParseException("(utils.py) extractPosition, invalid nmea Position, fix time has not a length of 6",line)
        
        try:
            timedFixTime = time(int(fixtimeString[0:2]), int(fixtimeString[2:4]), int(fixtimeString[4:6]))
        except ValueError as ve:
            raise LogParseException("(utils.py) extractPosition, invalid nmea Position, failed to cast fix time : "+str(ve),line)
    
    #print "    <"+str(longitudeDegree)+"><"+str(latitudeDegree)+"><"+str(timedFixTime)+">"
    return longitudeDegree,latitudeDegree,timedFixTime
        
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
        
        
    #TODO parse altitude and fixtime
        
        

