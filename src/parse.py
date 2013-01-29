#!/usr/bin/python

import os
from logstruct import NmeaLog, DumpLog
from dumpStruct import FileDump

nmeaLogDirectory = "/Volumes/Home/Downloads/root/nmea/log/"
nmeaLog = []
dumpLogDirectory = "/Volumes/Home/Downloads/root/dumper/log/"
dumpLog = []
dumpDirectory    = "/Volumes/Home/Downloads/root/dumper/dump/"
dump = []

#load nmea logs
for f in os.listdir(nmeaLogDirectory):
    if os.path.isfile(nmeaLogDirectory+f) and f.endswith(".log"):
        nmeaLog.append(NmeaLog(nmeaLogDirectory+f))
    else:
        print "warning, not a valid file : "+nmeaLogDirectory+f

#load dump logs
for f in os.listdir(dumpLogDirectory):
    if os.path.isfile(dumpLogDirectory+f) and f.endswith(".log"):
        dumpLog.append(DumpLog(dumpLogDirectory+f))
    else:
        print "warning, not a valid file : "+dumpLogDirectory+f

#load dump files 
for f in os.listdir(dumpDirectory):
    if os.path.isfile(dumpDirectory+f) and f.endswith(".txt"):
        dump.append(FileDump(dumpDirectory+f))
    else:
        print "warning, not a valid file : "+dumpDirectory+f
        
#correlate all structures
#TODO
