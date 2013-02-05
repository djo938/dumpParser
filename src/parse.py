#!/usr/bin/python

import os
from logstruct import NmeaLog, DumpLog, parseNmeaFile, parseDumpLogFile
from dumpStruct import FileDump
from datetime import timedelta
from dumpEvent import dumpNewDumpEvent
from nmeaEvent import nmeaNewPositionEvent
from logException import LogParseException

#nmeaLogDirectory = "/Volumes/Home/Downloads/root/nmea/log/"
nmeaLogDirectory = "/home/djo/developement/raw/nmea/log/"

#dumpLogDirectory = "/Volumes/Home/Downloads/root/dumper/log/"
dumpLogDirectory = "/home/djo/developement/raw/dumper/log/"

#dumpDirectory    = "/Volumes/Home/Downloads/root/dumper/dump/"
dumpDirectory    = "/home/djo/developement/raw/dumper/dump/"

kmlDirectory = "/home/djo/developement/raw/nmea/kml/"

KML_LINE_POINT_LIMIT = 200

############################################################################################################
###### DATA PARSING ########################################################################################
############################################################################################################
#load nmea logs
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
#update all the New position

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
#load dump logs
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
print "parsing dump..."
#load dump files 
dumpFiles = []
for fileName in os.listdir(dumpDirectory):
    if os.path.isfile(dumpDirectory+fileName) and fileName.endswith(".txt"):
        try:
            dumpFiles.append(FileDump(dumpDirectory+fileName))
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
    
    ### FIND A VALID ENTRY IN THE DUMP LOG ###
    
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
            dumpFile.eventLog = None
        elif len(dumpEventMatch) == 1: #one dump found, no need to try with a bigger limit
            dumpFile.eventLog = dumpEventMatch[0]
            dumpEventMatch[0].log.dumps.append(dumpFile)
            break
        elif len(dumpEventMatch) > 1: #several dump found, take the first and no need to try with a bigger limit
            #take the first, because there is no way to know which is the correct dump event
            print "    WARNING, several log correspondance for file "+dumpFile.File
            dumpFile.eventLog = dumpEventMatch[0]
            dumpEventMatch[0].log.dumps.append(dumpFile)
            for de in dumpEventMatch:
                print "        "+str(de.time)
            break
    
    #file without dump event matching ?
    if not isinstance(dumpFile.eventLog,dumpNewDumpEvent):   
        print "    WARNING, no dump log correspondance for file "+dumpFile.File
    
    ### FIND A VALID ENTRY IN THE NMEA LOG ###
    
    #if position and altitude is defined, find a valid nmea log    
    if dumpFile.longitude != None and dumpFile.latitude != None  and dumpFile.fixtime != None:
        for nmeaLog in nmeaLogs:
            for posEvent in nmeaLog.NewPosition:
                if posEvent.longitude != None and posEvent.latitude != None  and posEvent.fixtime != None:
                    #print dumpFile.longitude ," vs ", posEvent.longitude ," AND ", dumpFile.latitude ," vs ", posEvent.latitude ," AND ", dumpFile.fixtime ," vs ", posEvent.fixtime
                    if dumpFile.longitude == posEvent.longitude and dumpFile.latitude == posEvent.latitude and dumpFile.fixtime == posEvent.fixtime:
                        if dumpFile.nmeaEvent == None:#check colision
                            dumpFile.nmeaEvent = posEvent
                        else:
                            #WARNING, no colision management here
                            print "    WARNING, several position event to the dumpile : "+dumpFile.File
                    
                    #append the position 00000 in the whitoutGpsDataFiles
                        #Position : 0000.0000N 00000.0000E, fix time : 074407
                    if dumpFile.longitude == 0.0 and dumpFile.latitude == 0.0:
                        whitoutGpsFixFiles.append(dumpFile)
                    
                    
                        
        if not isinstance(dumpFile.nmeaEvent,nmeaNewPositionEvent):
            print "    WARNING, no nmea log correspondance for file "+dumpFile.File
    else:
        print "    no gps data for file "+dumpFile.File
        print "        "+str(dumpFile.eventLog.log)
        whitoutGpsDataFiles.append(dumpFile)
print "    Done !"
print ""

print "check linking integrity"
#check if all the dumps of a dump log are linked to the same nmea log
    #check also if a nmea log is linked to only one dump log

#build a dictionnary with all the nmea log linked to each dump log, in normal case, it should be one nmea
dumpLogDict = {}
for dumpFile in dumpFiles:
    if dumpFile.eventLog == None or dumpFile.nmeaEvent == None:
        continue
        
    if dumpFile.eventLog not in dumpLogDict:
        dumpLogDict[dumpFile.eventLog.log] = [dumpFile.nmeaEvent.log]
    else:
        dumpLogDict[dumpFile.eventLog.log].append(dumpFile.nmeaEvent.log)

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
            print "    WARNING, a nmealog is linked to several nmealog : "+str(item)
            #warning, no threatment
       
    
print "    Done !"
print ""
print "update dump files"
#update dump event
for dumpLog in dumpLogs: #pour tous les logs
    #print "dumlog file : ",dumpLog.File
    #collect diff time
    timeDelta = timedelta()
    timeDeltaCount = 0
    
    for dump in dumpLog.dumps: 

        if isinstance(dump.nmeaEvent,nmeaNewPositionEvent) and isinstance(dump.eventLog,dumpNewDumpEvent):
            diff = dump.eventLog.time - dump.nmeaEvent.time #temps ecoule entre le fix gps et le dump de la carte, on se base sur les mauvais temps
            #print "    diff : ",diff #varie entre 0 et 10 secondes si le gps est synchro
            
            dump.eventLog.newTime = dump.nmeaEvent.newTime + diff #on mets a jour le bon temps sur l'eventLog
            
            #calcule de la moyenne de diffrence entre le bon temps et le mauvais temps des eventlogs
            diff2 = dump.eventLog.newTime - dump.eventLog.time 
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
        #Position : 0000.0000N 00000.0000E, fix time : 074407  in list whitoutGpsFixFiles
        #Position : unknown  in list whitoutGpsDataFiles
            #for this kind of files, check if the dumpLog is linked to a nmeaLog, otherwise it will be impossible to find a position range
    
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

#TODO find the cablecar attached to each dump file


############################################################################################################
###### DATA SAVE ###########################################################################################
############################################################################################################

#TODO compute kml files
    #mettre une couleur par UID
    #mettre les lignes en rouge a partir de 13h

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
            kml.newlinestring(name=str(firstPos.newTime), description="", coords=tab)
            tab = []
            firstPos = None
            
    if len(tab) > 0:
        kml.newlinestring(name=str(firstPos.newTime), description="", coords=tab)
    
    if nmeaLog.dumpLog != None :
        for dump in nmeaLog.dumpLog.dumps:
            if dump.nmeaEvent.longitude == 0.0 and dump.nmeaEvent.latitude == 0.0:
                continue
        
            dumpTime = str(dump.eventLog.newTime.hour)+":"+str(dump.eventLog.newTime.minute)+":"+str(dump.eventLog.newTime.second)
            kml.newpoint(name="dump_"+str(dump.UID)+"_"+dumpTime, description="",coords=[(dump.nmeaEvent.longitude,dump.nmeaEvent.latitude)])
    else:
        print "warning, no dumpLog linked to "+str(nmeaLog)


kml.save(kmlDirectory+"skidump_"+str(currentNmeaLogDate.day)+"_"+str(currentNmeaLogDate.month)+"_"+str(currentNmeaLogDate.year)+".kml")

#TODO build csv files


#rewrite all the files
for d in dumpFiles:
    d.rewrite("/home/djo/developement/raw/dumper/dump/updated/")




