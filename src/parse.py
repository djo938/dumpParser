#!/usr/bin/python

import os
from logstruct import NmeaLog, DumpLog, parseNmeaFile, parseDumpLogFile
from dumpStruct import FileDump
from datetime import timedelta
from dumpEvent import dumpNewDumpEvent
from nmeaEvent import nmeaNewPositionEvent
from logException import LogParseException
from gpsUtils import *

#nmeaLogDirectory = "/Volumes/Home/Downloads/root/nmea/log/"
nmeaLogDirectory = "/home/djo/developement/raw/nmea/log/"

#dumpLogDirectory = "/Volumes/Home/Downloads/root/dumper/log/"
dumpLogDirectory = "/home/djo/developement/raw/dumper/log/"

#dumpDirectory    = "/Volumes/Home/Downloads/root/dumper/dump/"
dumpDirectory    = "/home/djo/developement/raw/dumper/dump/"

#kmlDirectory = "/Volumes/Home/Downloads/root/nmea/kml/"
kmlDirectory = "/home/djo/developement/raw/nmea/kml/"

KML_LINE_POINT_LIMIT = 200

############################################################################################################
###### DATA PARSING ########################################################################################
############################################################################################################

##### load nmea logs #######################################################################################
print "parsing nmea log..."
nmeaLogs = [] #store all the nmea log object
newPositionList = [] #store all the nmea New Position object from all the nmea logs

for fileName in os.listdir(nmeaLogDirectory):
    if os.path.isfile(nmeaLogDirectory+fileName) and fileName.endswith(".log"):
        newNmeaLogs = parseNmeaFile(nmeaLogDirectory+fileName)
        for nmeaLog in newNmeaLogs:
            newPositionList.extend(nmeaLog.NewPosition)
        nmeaLogs.extend(newNmeaLogs)
    else:
        print "    warning, not a valid file : "+nmeaLogDirectory+fileName
print "    log count : "+str(len(nmeaLogs))
print "    Done !"
print ""
print "update nmea log time"

##### update all the New position ##########################################################################
toRemove = []
for nmeaLog in nmeaLogs:
    if not nmeaLog.updateAllEventTime():
        toRemove.append(nmeaLog)

for nmeaLog in toRemove:
    nmeaLogs.remove(nmeaLog)
    
newPositionList = sorted(newPositionList) #sorte the new Position Event object on the corrected datetime
print "    Done !"
print ""
print "parsing dump log..."
dumpLogs = []

##### load dump logs ######################################################################################
for fileName in os.listdir(dumpLogDirectory):
    if os.path.isfile(dumpLogDirectory+fileName) and fileName.endswith(".log"):
        dumpLogs.extend(parseDumpLogFile(dumpLogDirectory+fileName))
    else:
        print "    warning, not a valid file : "+dumpLogDirectory+fileName

#count the dump event in all the dump logs
count = 0
for dumpLog in dumpLogs:
    #print str(len(dumpLog.dumpEvent))+" in "+dumpLog.File
    count += len(dumpLog.dumpEvent)

print "    log count : "+str(len(dumpLogs))
print "    Total dump : "+str(count)
print "    Done !"
print ""

##### load dump files ######################################################################################

print "parsing dump..."

dumpFiles = []
for fileName in os.listdir(dumpDirectory):
    if os.path.isfile(dumpDirectory+fileName) and fileName.endswith(".txt"):
        try:
            dumpFile = FileDump(dumpDirectory+fileName)
            dumpFile.dumpEvent = None
            dumpFile.nmeaEvent = None
            dumpFiles.append(dumpFile)
        except LogParseException as lpe:
            print "    "+str(lpe)+" at file "+dumpDirectory+fileName
    else:
        print "    warning, not a valid file : "+dumpDirectory+fileName

print "    dump count : "+str(len(dumpFiles))
print "    Done !"
print ""
############################################################################################################
###### DATA CORRELATION ####################################################################################
############################################################################################################

whitoutGpsDataFiles = [] #position : unknown
whitoutGpsFixFiles  = [] #position : 0000.0000
#link files with dump log
print "correlate data..."
for dumpFile in dumpFiles:
    
##### FIND A VALID ENTRY IN THE DUMP LOG ###################################################################
    
    for limite in range(1,3): #try perfect match, then 1 second math, and then 2 second match
        dumpEventMatch = [] #check the colision
        for dumpLog in dumpLogs: #for all log file
            for de in dumpLog.dumpEvent: #for all dump event
                #print "<"+dumpFile.UID+"> vs <"+de.UID+">"
                if dumpFile.UID == de.UID: #match on UID ?
                    dumpEventTime = de.time.time()
                    
                    dumpEventSeconds = (((dumpEventTime.hour * 60) + dumpEventTime.minute) * 60 ) + dumpEventTime.second
                    fileSeconds      = (((dumpFile.time.hour * 60) + dumpFile.time.minute) * 60 ) + dumpFile.time.second
                    diff = dumpEventSeconds - fileSeconds
                    
                    if diff < limite and diff > (-1 * limite): #match on time ?
                        #print "match"
                        dumpEventMatch.append(de)
                        #print str(dumpEventTime)+" vs "+str(dumpFile.time)
                           
        #check dumpEventMatch, if ==0, if > 1, if ==1
        if len(dumpEventMatch) == 0: #no dump found with this limit, try a bigger limit
            continue
        elif len(dumpEventMatch) == 1: #one dump found, no need to try with a bigger limit
            dumpFile.dumpEvent = dumpEventMatch[0]
            dumpEventMatch[0].log.dumps.append(dumpFile)
            break
        elif len(dumpEventMatch) > 1: #several dump found, take the first and no need to try with a bigger limit
            #take the first, because there is no way to know which is the correct dump event
            print "    WARNING, several log correspondance for file "+dumpFile.File
            dumpFile.dumpEvent = dumpEventMatch[0]
            dumpEventMatch[0].log.dumps.append(dumpFile)
            for de in dumpEventMatch:
                print "        "+str(de.time)
            break
    
    #file without dump event matching ?
    #if not isinstance(dumpFile.eventLog,dumpNewDumpEvent):   
    if dumpFile.dumpEvent == None:
        print "    WARNING, no dump log correspondance for file "+dumpFile.File
    
##### FIND A VALID ENTRY IN THE NMEA LOG ###################################################################
    
    #if position and altitude is defined, find a valid nmea log    
    if dumpFile.longitude != None and dumpFile.latitude != None  and dumpFile.fixtime != None:
        for nmeaLog in nmeaLogs:
            for posEvent in nmeaLog.NewPosition:
                if posEvent.longitude != None and posEvent.latitude != None  and posEvent.fixtime != None:
                    #print dumpFile.longitude ," vs ", posEvent.longitude ," AND ", dumpFile.latitude ," vs ", posEvent.latitude ," AND ", dumpFile.fixtime ," vs ", posEvent.fixtime
                    if dumpFile.longitude == posEvent.longitude and dumpFile.latitude == posEvent.latitude and dumpFile.fixtime == posEvent.fixtime:
                        #if dumpFile.nmeaEvent == None:#check colision
                        if dumpFile.nmeaEvent == None:#check colision
                            #dumpFile.nmeaEvent = posEvent
                            dumpFile.nmeaEvent = posEvent
                        else:
                            #WARNING, no colision management here
                            print "    WARNING, several position event to the dumpile : "+dumpFile.File
                    
        #append the position 00000 in the whitoutGpsDataFiles
            #Position : 0000.0000N 00000.0000E, fix time : 074407
        if dumpFile.longitude == 0.0 and dumpFile.latitude == 0.0:
            whitoutGpsFixFiles.append(dumpFile)
                    
                    
                        
        if dumpFile.nmeaEvent == None:
            print "    WARNING, no nmea log correspondance for file "+dumpFile.File
    else:
        print "    no gps data for file "+dumpFile.File
        if dumpFile.dumpEvent != None:
            print "        "+str(dumpFile.dumpEvent.log)
        else:
            print "        no dump log information"
        whitoutGpsDataFiles.append(dumpFile)
print "    file whitout gps fix : "+str(len(whitoutGpsFixFiles))
print "    file whitout gps data : "+str(len(whitoutGpsDataFiles))
print "    Done !"
print ""

##### check log links integrity ###################################################################
print "check linking integrity"
#check if all the dumps of a dump log are linked to the same nmea log
    #check also if a nmea log is linked to only one dump log

#build a dictionnary with all the nmea log linked to each dump log, in normal case, it should be one nmea
dumpLogDict = {}
for dumpFile in dumpFiles:
    if dumpFile.dumpEvent == None or dumpFile.nmeaEvent == None:
        continue
        
    if dumpFile.dumpEvent not in dumpLogDict:
        dumpLogDict[dumpFile.dumpEvent.log] = [dumpFile.nmeaEvent.log]
    else:
        dumpLogDict[dumpFile.dumpEvent.log].append(dumpFile.nmeaEvent.log)

nmeaLogDict = {}
for dumpLog,nmeaLogList in dumpLogDict.iteritems():
    if len(nmeaLogList) == 0:
        print "    WARNING, a dumplog is not linked to a nmea log : "+str(dumpLog)
        continue

    elif len(nmeaLogList) > 1:
        print "    WARNING, a dumplog is linked to several nmealog : "+str(dumpLog)
        #warning, no threatment
  
    else: #if len(nmeaLogList) == 1:
        dumpLog.nmeaLog = nmeaLogList[0]
        nmeaLogList[0].dumpLog = dumpLog
  
    for nmeaLog in nmeaLogList:
        if nmeaLog not in nmeaLogDict:
            nmeaLogDict[nmeaLog] = True
        else:
            print "    WARNING, a nmealog is linked to several dumplog : "+str(nmeaLog)
            #warning, no threatment
       
    
print "    Done !"
print ""

##### update dump datetime ###################################################################
print "update dump files"
#update dump event
for dumpLog in dumpLogs: #pour tous les logs
    #print "dumlog file : ",dumpLog.File
    #collect diff time
    timeDelta = timedelta()
    timeDeltaCount = 0
    
    for dumpFile in dumpLog.dumps: 

        #if isinstance(dump.nmeaEvent,nmeaNewPositionEvent) and isinstance(dump.eventLog,dumpNewDumpEvent):
        if dumpFile.nmeaEvent != None and dumpFile.dumpEvent != None:
        
            diff = dumpFile.dumpEvent.time - dumpFile.nmeaEvent.time #temps ecoule entre le fix gps et le dump de la carte, on se base sur les mauvais temps
            #print "    diff : ",diff #varie entre 0 et 10 secondes si le gps est synchro
            
            dumpFile.dumpEvent.newTime = dumpFile.nmeaEvent.newTime + diff #on mets a jour le bon temps sur l'eventLog
            dumpFile.datetime = dumpFile.dumpEvent.newTime
            #calcule de la moyenne de diffrence entre le bon temps et le mauvais temps des eventlogs
            diff2 = dumpFile.dumpEvent.newTime - dumpFile.dumpEvent.time 
            #print "    diff2 : ",diff2
            timeDelta += diff2
            timeDeltaCount += 1
            
    if timeDeltaCount > 0:
        timeDelta /= timeDeltaCount
        
    
        
    #print "    delta : ",timeDelta
    
    #mise a jour de tous les dumpEvent, y compris ceux qui n'ont pas de data gps
    for dEvent in dumpLog.dumpEvent:
        if dEvent.newTime == None:
            dEvent.newTime = dEvent.time + timeDelta
            
#TODO compute gps position for the file without gps data
    #Position : 0000.0000N 00000.0000E, fix time : 074407  in list whitoutGpsFixFiles (16 items)
    #Position : unknown  in list whitoutGpsDataFiles (6 items)
        #for this kind of files, check if the dumpLog is linked to a nmeaLog, otherwise it will be impossible to find a position range
        
    #not realy a priority thing...
    
    """for d in whitoutGpsDataFiles:
    
    #TODO find the previous and the next nearest position
    #newPositionList
    low = 0
    hight = len(newPositionList)
    mid = (low + hight) // 2
    
    while low < hight:
        mid = (low + hight) // 2
        if newPositionList[mid].newTime == d.eventLog.newTime:
            #Match
            print mid
            break
        elif newPositionList[mid].newTime < d.eventLog.newTime:
            low = mid+1
        else: #newPositionList[mid].newTime > d.eventLog.newTime:
            hight = mid
    print low,hight"""
print "    Done !"
print "linked gps data to cable car"
#find the cablecar attached to each dump file
gondolaMatch = 0
gondolaNotMatch = 0

pausePoint = [gpsPoint(45.324157,6.53898),gpsPoint(45.377333,6.504793),gpsPoint(45.380217,6.504257),gpsPoint(45.382075,6.5027),gpsPoint(45.381098,6.503282)]

for dumpFile in dumpFiles:
    if dumpFile.latitude != None and dumpFile.latitude != 0.0 and dumpFile.longitude != None and dumpFile.longitude != 0.0:
        gondola = findThenearestLine(  dumpFile.latitude,  dumpFile.longitude  )
        
        #check if the position is not a pause area (lunchtime, etc.)
        pause = False
        for ppoint in pausePoint:
            if getDistance(dumpFile.latitude,  dumpFile.longitude,ppoint.latitude,  ppoint.longitude) < 0.010:
                pause = True
                
        if pause:
            continue

        dumpFile.cablecarInformation = gondola

        if gondola[0] > 0.020:
            print "    Warning, long distance match : lat="+str(dumpFile.latitude)+", lon="+str(dumpFile.longitude)+str(  gondola   )
            gondolaNotMatch +=1
        else:
            #afficher quand la distance est prise du sommet, c'est peu etre anormal
            if gondola[0] == 2:
                print "    Warning, match at the endStation : lat="+str(dumpFile.latitude)+", lon="+str(dumpFile.longitude)+str(  gondola   )
            gondolaMatch +=1

print "    gondolaPerfectMatch="+str(gondolaMatch)
print "    gondolaAbnormalMatch="+str(gondolaNotMatch)
print "    Done !"

############################################################################################################
###### DATA SAVE ###########################################################################################
############################################################################################################

#BUILD KML FILES
UIDtoColor = {"E016246604C06B7A" : "http://maps.gstatic.com/mapfiles/ms2/micons/red-dot.png", 
              "E016246604C06BA0" : "http://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png", 
              "E016246604C070DE" : "http://maps.gstatic.com/mapfiles/ms2/micons/yellow-dot.png", 
              "E016246604C0862C" : "http://maps.gstatic.com/mapfiles/ms2/micons/green-dot.png", 
              "E016246604C0938B" : "http://maps.gstatic.com/mapfiles/ms2/micons/pink-dot.png", 
              "E016246604C05492" : "http://maps.gstatic.com/mapfiles/ms2/micons/ltblue-dot.png", 
              "E016246604C09352" : "http://maps.gstatic.com/mapfiles/ms2/micons/orange-dot.png", 
              "E0162466025BF373" : "http://maps.gstatic.com/mapfiles/ms2/micons/purple-dot.png"}

def sortNneaList(x,y):
    return int( (x.dateEvent.newTime - y.dateEvent.newTime).total_seconds() ) #warning, this method don care about milli and microseconds

nmeaLogs = sorted(nmeaLogs,cmp=sortNneaList)

from simplekml import Kml
kml = Kml()

currentNmeaLogDate = None
for nmeaLog in nmeaLogs:
    if currentNmeaLogDate == None:
        currentNmeaLogDate = nmeaLog.dateEvent.newTime
    elif nmeaLog.dateEvent.newTime.day != currentNmeaLogDate.day or nmeaLog.dateEvent.newTime.month != currentNmeaLogDate.month or nmeaLog.dateEvent.newTime.year != currentNmeaLogDate.year:
        kml.save(kmlDirectory+"skidump_"+str(currentNmeaLogDate.day)+"_"+str(currentNmeaLogDate.month)+"_"+str(currentNmeaLogDate.year)+".kml")
        currentNmeaLogDate = nmeaLog.dateEvent.newTime
        kml = Kml()

    tab = []
    firstPos = None
    for position in nmeaLog.NewPosition:
        if firstPos == None:
            firstPos = position
    
        #ne pas mettre les 0.0
        if position.longitude == 0.0 and position.latitude == 0.0:
            continue
    
        tab.append( ( position.longitude,position.latitude) )
        
        if len(tab) == KML_LINE_POINT_LIMIT:
            line = kml.newlinestring(name=str(firstPos.newTime), description="", coords=tab)
            tab = []
            
            
            if firstPos.newTime.hour < 12 or (firstPos.newTime.hour == 12 and firstPos.newTime.minute < 30):
                #blue line
                line.style.linestyle.color = 'ffff0000'
                
            else:
                #red line
                line.style.linestyle.color = 'ff0000ff'
                
            firstPos = None
                
    if len(tab) > 0:
        line = kml.newlinestring(name=str(firstPos.newTime), description="", coords=tab)
        
        if firstPos.newTime.hour < 12 or (firstPos.newTime.hour == 12 and firstPos.newTime.minute < 30):
            #blue line
            line.style.linestyle.color = 'ffff0000'
            
        else:
            #red line
            line.style.linestyle.color = 'ff0000ff'
    
    if nmeaLog.dumpLog != None :
        for dumpFile in nmeaLog.dumpLog.dumps:
            if dumpFile.nmeaEvent.longitude == 0.0 and dumpFile.nmeaEvent.latitude == 0.0:
                continue
        
            dumpTime = str(dumpFile.dumpEvent.newTime.hour)+":"+str(dumpFile.dumpEvent.newTime.minute)+":"+str(dumpFile.dumpEvent.newTime.second)
            point = kml.newpoint(name="dump_"+str(dumpFile.UID)+"_"+dumpTime, description="",coords=[(dumpFile.longitude,dumpFile.latitude)])
            
            if dumpFile.UID in UIDtoColor:
                 point.style.iconstyle.icon.href = UIDtoColor[dumpFile.UID]
            else:
                print "warning unknown UID : "+str(dumpFile.UID)

    else:
        print "warning, no dumpLog linked to "+str(nmeaLog)


kml.save(kmlDirectory+"skidump_"+str(currentNmeaLogDate.day)+"_"+str(currentNmeaLogDate.month)+"_"+str(currentNmeaLogDate.year)+".kml")

#build a file with all the cable car
kml = Kml()
for line in lineList:
    kml.newlinestring(name=str(firstPos.newTime), description="", coords=[(line.startPoint.longitude,line.startPoint.latitude),(line.endPoint.longitude,line.endPoint.latitude)])
    
kml.save(kmlDirectory+"cablecar.kml")

#build csv files
csvFiles = open("./output"+".csv", 'w')
csvFiles.write("UID;date;hour;minute seconds;position;cablecar;accuracy;data\n")
sectorToGet = [0x02,0x2f,0x30,0x31]
for dumpFile in dumpFiles:
    if dumpFile.cablecarInformation == None:
        continue
    
    dataString = ""
    
    for i in sectorToGet:
        value = dumpFile.getSector(i)
        tmpString = bin(value)
        tmpString = tmpString[2:]
        zeroToAdd = 32 - len(tmpString)
        for i in range(0,zeroToAdd):
            tmpString = "0"+tmpString
        
        dataString += tmpString+" "
    
    csvFiles.write(str(dumpFile.UID)+";"+dumpFile.dumpEvent.newTime.strftime("%d %A %B %Y %H:%M:%S")+";"+dumpFile.dumpEvent.newTime.strftime("%d %A %B %Y %H:%M:%S")+";"+dumpFile.dumpEvent.newTime.strftime("%d %A %B %Y %H:%M:%S")+";"+str(dumpFile.latitude)+" "
    +str(dumpFile.longitude)+";"+dumpFile.cablecarInformation[2]+";"+str((dumpFile.cablecarInformation[0]*1000))+" meters "+dumpFile.cablecarInformation[1]+";"+dataString+"\n")

csvFiles.close()

#rewrite all the files
for dumpFile in dumpFiles:
    dumpFile.rewrite("/home/djo/developement/raw/dumper/dump/updated/")




