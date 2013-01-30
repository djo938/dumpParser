#!/usr/bin/python

def extractPosition(line):
    line = line.strip()
    splittedDoublePoint = line.split(":")
    
    if len(splittedDoublePoint) != 3 and len(splittedDoublePoint) != 2:
        print "(extractPosition) WARNING, invalid nmea Position, double point split : "+str(line)
        return None,None,None
        
    #latitude-longitude
    splittedDoublePoint[1] = splittedDoublePoint[1].strip()
    splittedSpace = splittedDoublePoint[1].split(" ")
    
    if len(splittedDoublePoint) != 2:
        if len(splittedSpace) != 4:
            print "(extractPosition) WARNING, invalid nmea Position, space split : "+str(line)
            return None,None,None
            
        #self.longitude = splittedSpace[0]
        #self.latitude  = splittedSpace[1][:-1]
        
        #fix time
        splittedDoublePoint[2] = splittedDoublePoint[2].strip()
        if len(splittedDoublePoint[2]) != 6:
            print "(extractPosition) WARNING, invalid nmea Position, fix time length : "+str(line)
            return None,None,None
            
        #self.fixtime = splittedDoublePoint[2]
        #self.hour    = line[-6:-4]
        #self.minute  = line[-4:-2]
        #self.seconds = line[-2:][:2]
        
        return splittedSpace[0],splittedSpace[1][:-1],splittedDoublePoint[2]
    else:
        if len(splittedSpace) != 2:
            print "(extractPosition) WARNING, invalid nmea Position, space split : "+str(line)
            return None,None,None
            
        #self.longitude = splittedSpace[0]
        #self.latitude  = splittedSpace[1]
        #self.fixtime = None
        
        return splittedSpace[0],splittedSpace[1],None
        
def extractAltitude(line):
    line = line.strip()
    splittedDoublePoint = line.split(":")
    
    if len(splittedDoublePoint) != 3 and len(splittedDoublePoint) != 2:
        print "(extractAltitude) WARNING, invalid nmea altitude, double point split : "+str(line)
        return None,None,None
    
    #altitude
    splittedDoublePoint[1] = splittedDoublePoint[1].strip()
    splittedSpace = splittedDoublePoint[1].split(" ")
    
    if len(splittedDoublePoint) != 2:
        if len(splittedSpace) != 4:
            print "(extractAltitude) WARNING, invalid nmea altitude, space split : "+str(line)
            return None,None,None
    
        altitude = None
        try:
            altitude = float(splittedSpace[0])
        except ValueError as va:
            print "(extractAltitude) WARNING, invalid nmea altitude, float cast : "+str(line)+" "+str(va)
            return None,None,None
        
        #units
        #self.unit = splittedSpace[1][:-1]
    
        #fix time
        splittedDoublePoint[2] = splittedDoublePoint[2].strip()
        if len(splittedDoublePoint[2]) != 6:
            print "(extractAltitude) WARNING, invalid nmea altitude, fix time length : "+str(line)
            return None,None,None
            
        #self.fixtime = splittedDoublePoint[2]
        
        return altitude, splittedSpace[1][:-1], splittedDoublePoint[2]
    else:
        if len(splittedSpace) != 2:
            print "(extractAltitude) WARNING, invalid nmea altitude, space split : "+str(line)
            return None,None,None
            
        altitude = None
        try:
            altitude = float(splittedSpace[0])
        except ValueError as va:
            print "(extractAltitude) WARNING, invalid nmea altitude, float cast : "+str(line)+" "+str(va)
            return None,None,None
        
        #units
        #self.unit = splittedSpace[1]
        #self.fixtime = None
        
        return altitude, splittedSpace[1], None
        

