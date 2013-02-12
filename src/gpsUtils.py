#!/usr/bin/python

#http://www.movable-type.co.uk/scripts/latlong.html

from math import *
import sys

R = 6371.000

def getDistance(pointALat,pointALon, pointBLat, pointBLon):
    dLat = radians( (pointBLat-pointALat) )
    dLon = radians( (pointBLon-pointALon) )
    lat1 = radians( pointALat )
    lat2 = radians( pointBLat )

    a = sin(dLat/2.0) * sin(dLat/2.0) + sin(dLon/2.0) * sin(dLon/2.0) * cos(lat1) * cos(lat2); 
    c = 2.0 * atan2(sqrt(a), sqrt(1.0-a)); 
    d = R * c;
    
    return d

class gpsPoint(object):
    def __init__(self,latitude,longitude):
        self.latitude = latitude
        self.longitude = longitude
        
class gpsLine(object):
    def __init__(self,startPoint,endPoint,name=None):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.name = name
        
        self.segmentLength = getDistance(startPoint.latitude,startPoint.longitude,endPoint.latitude,endPoint.longitude)

class cableCar(gpsLine):
    def __init__(self,startPoint,endPoint,name,sectorName):
        gpsLine.__init__(self,startPoint,endPoint,name)
        self.sectorName = sectorName
        
    def __str__(self):
        return self.name +" on area "+self.sectorName
        
    def __repr__(self):
        return str(self)
        
lineList = []

lineList.append(cableCar(gpsPoint(45.376726,6.504472),gpsPoint(45.373195,6.528719),"saint martin 1","les menuires"))
lineList.append(cableCar(gpsPoint(45.372588,6.528923),gpsPoint(45.364652,6.55721),"saint martin 2","les menuires"))
lineList.append(cableCar(gpsPoint(45.33416,6.555386),gpsPoint(45.337463,6.5712),"roc des 3 marches 2","les menuires"))
lineList.append(cableCar(gpsPoint(45.322468,6.538998),gpsPoint(45.330634,6.555134),"roc des 3 marches 1","les menuires"))
lineList.append(cableCar(gpsPoint(45.326493,6.552784),gpsPoint(45.331233,6.571055),"becca","les menuires"))
lineList.append(cableCar(gpsPoint(45.319179,6.535564),gpsPoint(45.311091,6.519954),"la masse 1","les menuires"))
lineList.append(cableCar(gpsPoint(45.315075,6.516553),gpsPoint(45.29721,6.50849),"la masse 2","les menuires"))
lineList.append(cableCar(gpsPoint(45.319361,6.535257),gpsPoint(45.319296,6.550181),"doron","les menuires"))
lineList.append(cableCar(gpsPoint(45.319934,6.550109),gpsPoint(45.319032,6.578409),"mont de la chambre","les menuires"))
lineList.append(cableCar(gpsPoint(45.353947,6.55383),gpsPoint(45.338353,6.572643),"granges","les menuires"))

lineList.append(cableCar(gpsPoint(45.392064,6.568234),gpsPoint(45.393895,6.575417),"rhodos 1","meribel"))
lineList.append(cableCar(gpsPoint(45.393993,6.575894),gpsPoint(45.396393,6.585368),"rhodos 2","meribel"))
lineList.append(cableCar(gpsPoint(45.376843,6.56339),gpsPoint(45.364169,6.557864),"tougnette 2","meribel"))
lineList.append(cableCar(gpsPoint(45.390942,6.567965),gpsPoint(45.377205,6.563551),"tougnette 1","meribel"))
lineList.append(cableCar(gpsPoint(45.389137,6.58871),gpsPoint(45.383331,6.610173),"saulire express 2","meribel"))
lineList.append(cableCar(gpsPoint(45.39145,6.567123),gpsPoint(45.389242,6.588401),"saulire express 1","meribel"))
lineList.append(cableCar(gpsPoint(45.371846,6.580803),gpsPoint(45.342123,6.577758),"plattieres express","meribel mottaret"))
lineList.append(cableCar(gpsPoint(45.402461,6.586923),gpsPoint(45.407591,6.602228),"loze","meribel"))
lineList.append(cableCar(gpsPoint(45.390686,6.552548),gpsPoint(45.392675,6.536246),"olympics","meribel"))
lineList.append(cableCar(gpsPoint(45.391168,6.567225),gpsPoint(45.390177,6.552038),"roc de fer","meribel"))
lineList.append(cableCar(gpsPoint(45.372547,6.573308),gpsPoint(45.367222,6.560954),"table verte","meribel mottaret"))
lineList.append(cableCar(gpsPoint(45.371976,6.580375),gpsPoint(45.363508,6.571129),"combes","meribel mottaret"))
lineList.append(cableCar(gpsPoint(45.372408,6.5801),gpsPoint(45.370324,6.570186),"arroles","meribel mottaret"))

lineList.append(cableCar(gpsPoint(45.29544,6.575934),gpsPoint(45.291651,6.614129),"funitel de peclet","val thorens"))
lineList.append(cableCar(gpsPoint(45.27302,6.605385),gpsPoint(45.26823,6.615746),"glacier de thorens","val thorens"))
lineList.append(cableCar(gpsPoint(45.294029,6.564615),gpsPoint(45.281023,6.56262),"caron","val thorens"))
lineList.append(cableCar(gpsPoint(45.280555,6.562598),gpsPoint(45.263672,6.560249),"cime caron","val thorens"))
lineList.append(cableCar(gpsPoint(45.280955,6.568134),gpsPoint(45.266293,6.58044),"grand fond","val thorens"))
lineList.append(cableCar(gpsPoint(45.272084,6.592103),gpsPoint(45.2659,6.595686),"thorens","val thorens"))
lineList.append(cableCar(gpsPoint(45.2951,6.577447),gpsPoint(45.291138,6.594463),"cascades","val thorens"))
lineList.append(cableCar(gpsPoint(45.284352,6.583412),gpsPoint(45.271933,6.591373),"portette","val thorens"))
lineList.append(cableCar(gpsPoint(45.287613,6.583402),gpsPoint(45.2729,6.606275),"moraine","val thorens"))

lineList.append(cableCar(gpsPoint(45.414908,6.632746),gpsPoint(45.406272,6.614153),"chenus","courchevel"))
lineList.append(cableCar(gpsPoint(45.406397,6.629554),gpsPoint(45.39281,6.624791),"biolay","courchevel"))
lineList.append(cableCar(gpsPoint(45.378535,6.633513),gpsPoint(45.37153,6.64502),"chanrossa","courchevel"))
lineList.append(cableCar(gpsPoint(45.390444,6.63001),gpsPoint(45.382325,6.615655),"suisses","courchevel"))
lineList.append(cableCar(gpsPoint(45.392125,6.642204),gpsPoint(45.388534,6.632832),"gravelles","courchevel"))

lineList.append(cableCar(gpsPoint(45.406235,6.612431),gpsPoint(45.406969,6.602748),"col de la loze","courchevel"))
lineList.append(cableCar(gpsPoint(45.415924,6.607077),gpsPoint(45.407726,6.602888),"dou des lanches","courchevel"))
lineList.append(cableCar(gpsPoint(45.43164,6.597647),gpsPoint(45.417231,6.609373),"la tania","courchevel"))


#lineList.append(cableCar(gpsPoint(),gpsPoint(),""))
#lineList.append(cableCar(gpsPoint(),gpsPoint(),""))

def getBearing(pointALat,pointALon, pointBLat, pointBLon):
    dLat = radians( (pointBLat-pointALat) )
    dLon = radians( (pointBLon-pointALon) )
    lat1 = radians( pointALat )
    lat2 = radians( pointBLat )

    y = sin(dLon) * cos(lat2);
    x = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dLon);

    return degrees ( atan2(y, x) )
    
def getLineDistance(pointXLat,pointXLon,linePointALat,linePointALon,linePointBLat,linePointBLon):
    
    d13 = getDistance(linePointALat,linePointALon,pointXLat,pointXLon)
    brng13 = radians( getBearing(linePointALat,linePointALon,pointXLat,pointXLon) )
    brng12 = radians( getBearing(linePointALat,linePointALon,linePointBLat,linePointBLon) )
    
    return asin(sin(d13/R)*sin(brng13-brng12)) * R;

def sortDistance(x,y):
    disX,ditType,nameX = x
    disY,ditType,nameY = y
    
    return int(disX-disY)

DISTANCEFROMLINE = "from line"
DISTANCEFROMSTARTPOINT = "from starting point"
DISTANCEFROMENDPOINT = "from end point"

def findThenearestLine(pointXLat,pointXLon):
    nearest = (sys.maxint,DISTANCEFROMLINE,"the farest")
    for line in lineList:
        #print line.name
        
        distanceFromStartPoint = getDistance(pointXLat,pointXLon,line.startPoint.latitude,line.startPoint.longitude)
        distanceFromEndPoint = getDistance(pointXLat,pointXLon,line.endPoint.latitude,line.endPoint.longitude)
        
        #print "    distanceFromStartPoint="+str(distanceFromStartPoint)
        #print "    distanceFromEndPoint="+str(distanceFromEndPoint)
        #print "    segmentLength="+str(line.segmentLength)
        
        distanceFromTheLine = getLineDistance(pointXLat,pointXLon,line.startPoint.latitude,line.startPoint.longitude,line.endPoint.latitude,line.endPoint.longitude )
        
        #print "    distanceFromTheLine="+str(distanceFromTheLine)
        
        if distanceFromTheLine < 0.0:
            distanceFromTheLine *= -1
            
        if sqrt( distanceFromStartPoint**2 - distanceFromTheLine**2 ) > line.segmentLength or sqrt( distanceFromEndPoint**2 - distanceFromTheLine**2 ) > line.segmentLength:
            #print "    not on the segment"
            
            #on prend la plus petite distance par rapport aux gares
            if distanceFromStartPoint < distanceFromEndPoint:
                distance = distanceFromStartPoint
                distanceType = DISTANCEFROMSTARTPOINT
            else:
                distance = distanceFromEndPoint
                distanceType = DISTANCEFROMENDPOINT
        else:
            #print "    on the segment"    
            
            #on prend la distance a partir de la ligne
            distance = distanceFromTheLine
            distanceType = DISTANCEFROMLINE
    
        if distance < nearest[0]:
            nearest = (distance,distanceType,line)
    
    return nearest



