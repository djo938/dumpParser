#!/usr/bin/python

import os
from logstruct import NmeaLog, DumpLog, parseNmeaFile, parseDumpLogFile
from dumpStruct import FileDump
from datetime import timedelta
from dumpEvent import dumpNewDumpEvent
from nmeaEvent import nmeaNewPositionEvent

#nmeaLogDirectory = "/Volumes/Home/Downloads/root/nmea/log/"
nmeaLogDirectory = "/home/djo/developement/raw/nmea/log/"

#dumpLogDirectory = "/Volumes/Home/Downloads/root/dumper/log/"
dumpLogDirectory = "/home/djo/developement/raw/dumper/log/"

#dumpDirectory    = "/Volumes/Home/Downloads/root/dumper/dump/"
dumpDirectory    = "/home/djo/developement/raw/dumper/dump/"



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
        print "warning, not a valid file : "+nmeaLogDirectory+fileName

#update all the New position 
for nmeaLog in nmeaLogs:
    nmeaLog.updateAllEventTime()
    
newPositionList = sorted(newPositionList) #sorte the new Position Event object on the corrected datetime
print "DONE !"

print "parsing dump log..."
dumpLogs = []
#load dump logs
for fileName in os.listdir(dumpLogDirectory):
    if os.path.isfile(dumpLogDirectory+fileName) and fileName.endswith(".log"):
        dumpLogs.extend(parseDumpLogFile(dumpLogDirectory+fileName))
    else:
        print "warning, not a valid file : "+dumpLogDirectory+fileName

#count the dump event in all the dump logs
count = 0
for dumpLog in dumpLogs:
    #print str(len(dumpLog.dumpEvent))+" in "+dumpLog.File
    count += len(dumpLog.dumpEvent)

print "TOTAL dump : "+str(count)
print "DONE !"

print "parsing dump..."
#load dump files 
dumpFiles = []
for fileName in os.listdir(dumpDirectory):
    if os.path.isfile(dumpDirectory+fileName) and fileName.endswith(".txt"):
        dumpFiles.append(FileDump(dumpDirectory+fileName))
    else:
        print "warning, not a valid file : "+dumpDirectory+fileName
        
print "DONE !"

############################################################################################################
###### DATA CORRELATION ####################################################################################
############################################################################################################

whitoutGpsDataFiles = []

#link files with dump log
for dumpFile in dumpFiles:
    
    ### FIND A VALID ENTRY IN THE DUMP LOG ###
    
    for limite in range(1,3): #try perfect match, then 1 second math, and then 2 second match
        dumpEventMatch = []
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
            print "WARNING, several log correspondance for file "+dumpFile.File
            dumpFile.eventLog = dumpEventMatch[0]
            dumpEventMatch[0].log.dumps.append(dumpFile)
            for de in dumpEventMatch:
                print "    "+str(de.time)
            break
    
    #file without dump event matching ?
    if not isinstance(dumpFile.eventLog,dumpNewDumpEvent):
        print "WARNING, no dump log correspondance for file "+dumpFile.File
    
    ### FIND A VALID ENTRY IN THE NMEA LOG ###
    
    #if position and altitude is defined, find a valid nmea log
    
    if dumpFile.longitude != None and dumpFile.latitude != None  and dumpFile.fixtime != None:
        for nmeaLog in nmeaLogs:
            for posEvent in nmeaLog.NewPosition:
                if posEvent.longitude != None and posEvent.latitude != None  and posEvent.fixtime != None:
                    if dumpFile.longitude == posEvent.longitude and dumpFile.latitude == posEvent.latitude and dumpFile.fixtime == posEvent.fixtime:
                        dumpFile.nmeaEvent = posEvent
        if not isinstance(dumpFile.nmeaEvent,nmeaNewPositionEvent):
            print "WARNING, no nmea log correspondance for file "+dumpFile.File        
    else:
        print "no gps date for file "+dumpFile.File
        whitoutGpsDataFiles.append(dumpFile)

#update dump event
for dumpLog in dumpLogs: #pour tous les logs
    print "dumlog file : ",dumpLog.File
    #collect diff time
    timeDelta = timedelta()
    timeDeltaCount = 0
    
    for d in dumpLog.dumps: 

        if isinstance(d.nmeaEvent,nmeaNewPositionEvent) and isinstance(d.eventLog,dumpNewDumpEvent):
            diff = d.eventLog.time - d.nmeaEvent.time #temps ecoule entre le fix gps et le dump de la carte
            #print "    diff : ",diff #varie entre 0 et 10 secondes si le gps est synchro
            
            d.eventLog.newTime = d.nmeaEvent.newTime + diff
            
            diff2 = d.eventLog.newTime - d.eventLog.time
            #print "    diff2 : ",diff2
            timeDelta += diff2
            timeDeltaCount += 1
            
    if timeDeltaCount > 0:
        timeDelta /= timeDeltaCount
        
    #print "    delta : ",timeDelta
    
    for dEvent in dumpLog.dumpEvent:
        if dEvent.newTime == None:
            dEvent.newTime = dEvent.time + timeDelta
            
    #TODO compute gps position for the file without gps data
        #Position : 0000.0000N 00000.0000E, fix time : 074407 (not yet in the list)
        #Position : unknown (already in the list)
    
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

############################################################################################################
###### DATA SAVE ###########################################################################################
############################################################################################################

#TODO compute kml files
    #one files per day
    #dump event



#rewrite all the files
for d in dumpFiles:
    d.rewrite("/home/djo/developement/raw/dumper/dump/updated/")




