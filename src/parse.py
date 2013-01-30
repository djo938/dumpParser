#!/usr/bin/python

import os
from logstruct import NmeaLog, DumpLog, parseNmeaFile, parseDumpLogFile
from dumpStruct import FileDump
from datetime import timedelta
from dumpEvent import dumpNewDumpEvent
from nmeaEvent import nmeaNewPositionEvent

#nmeaLogDirectory = "/Volumes/Home/Downloads/root/nmea/log/"
nmeaLogDirectory = "/home/djo/developement/raw/nmea/log/"
nmeaLog = []
#dumpLogDirectory = "/Volumes/Home/Downloads/root/dumper/log/"
dumpLogDirectory = "/home/djo/developement/raw/dumper/log/"
dumpLog = []
#dumpDirectory    = "/Volumes/Home/Downloads/root/dumper/dump/"
dumpDirectory    = "/home/djo/developement/raw/dumper/dump/"
dump = []
newPositionList = []

#load nmea logs
print "parsing nmea log..."
for f in os.listdir(nmeaLogDirectory):
    if os.path.isfile(nmeaLogDirectory+f) and f.endswith(".log"):
        lnmea = parseNmeaFile(nmeaLogDirectory+f)
        for log in lnmea:
            newPositionList.extend(log.NewPosition)
        nmeaLog.extend(lnmea)
    else:
        print "warning, not a valid file : "+nmeaLogDirectory+f

#update all the New position 
for log in nmeaLog:
    log.updateAllEventTime()
    
newPositionList = sorted(newPositionList)
print "DONE !"

print "parsing dump log..."
#load dump logs
for f in os.listdir(dumpLogDirectory):
    if os.path.isfile(dumpLogDirectory+f) and f.endswith(".log"):
        dumpLog.extend(parseDumpLogFile(dumpLogDirectory+f))
    else:
        print "warning, not a valid file : "+dumpLogDirectory+f

count = 0
for dl in dumpLog:
    #print str(len(dl.dumpEvent))+" in "+dl.File
    count += len(dl.dumpEvent)

print "TOTAL dump : "+str(count)
print "DONE !"

print "parsing dump..."
#load dump files 
for f in os.listdir(dumpDirectory):
    if os.path.isfile(dumpDirectory+f) and f.endswith(".txt"):
        dump.append(FileDump(dumpDirectory+f))
    else:
        print "warning, not a valid file : "+dumpDirectory+f
        
print "DONE !"

#correlate all structures

#TODO make a big list with all New Position


whitoutGpsDataFiles = []

#link files with dump log
for d in dump:
    #find a valid dumplog
    for limite in range(1,3): #try perfect math, then 1 second math, and then 2 second match
        dumpEventMatch = []
        for dl in dumpLog:
            for de in dl.dumpEvent:
                #print "<"+d.UID+"> vs <"+de.UID+">"
                if d.UID == de.UID:
                    dumpEventTime = de.time.time()
                    
                    dumpEventSeconds = (((dumpEventTime.hour * 60) + dumpEventTime.minute) * 60 ) + dumpEventTime.second
                    fileSeconds      = (((d.time.hour * 60) + d.time.minute) * 60 ) + d.time.second
                    diff = dumpEventSeconds - fileSeconds
                    
                    if diff < limite and diff > (-1 * limite):
                        #print "match"
                        dumpEventMatch.append(de)
                        #print str(dumpEventTime)+" vs "+str(d.time)
                           
        #check dumpEventMatch, if ==0, if > 1, if ==1
        if len(dumpEventMatch) == 0:
            d.eventLog = None
        elif len(dumpEventMatch) == 1:
            d.eventLog = dumpEventMatch[0]
            dumpEventMatch[0].log.dumps.append(d)
            break
        elif len(dumpEventMatch) > 1:
            print "WARNING, several log correspondance for file "+d.File
            d.eventLog = dumpEventMatch[0]
            dumpEventMatch[0].log.dumps.append(d)
            for de in dumpEventMatch:
                print "    "+str(de.time)
            break
    
    if not isinstance(d.eventLog,dumpNewDumpEvent):
        print "WARNING, no dump log correspondance for file "+d.File
    
    #if position and altitude is defined, find a valid nmea log
    d.nmeaEvent = None
    if d.longitude != None and d.latitude != None  and d.fixtime != None:
        for nl in nmeaLog:
            for posEvent in nl.NewPosition:
                if posEvent.longitude != None and posEvent.latitude != None  and posEvent.fixtime != None:
                    if d.longitude == posEvent.longitude and d.latitude == posEvent.latitude and d.fixtime == posEvent.fixtime:
                        d.nmeaEvent = posEvent
        if not isinstance(d.nmeaEvent,nmeaNewPositionEvent):
            print "WARNING, no nmea log correspondance for file "+d.File        
    else:
        print "no gps date for file "+d.File
        whitoutGpsDataFiles.append(d)

#update dump event
for dl in dumpLog: #pour tous les logs
    print "dumlog file : ",dl.File
    #collect diff time
    timeDelta = timedelta()
    timeDeltaCount = 0
    
    for d in dl.dumps: 

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
    
    for dEvent in dl.dumpEvent:
        if dEvent.newTime == None:
            dEvent.newTime = dEvent.time + timeDelta

#TODO compute gps position for the file without gps data
#

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

#rewrite all the files
for d in dump:
    d.rewrite("/home/djo/developement/raw/dumper/dump/updated/")




