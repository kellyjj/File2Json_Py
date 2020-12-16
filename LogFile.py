#kelly j,  10-14-2020
#this will have the logging functions needed by code.
#this will also have the class ErrorMsg, which will be what the logging class will write out
#keeping in the same file since the two go together.
#

from enum import Enum
from datetime import date
from xml.dom import minidom 
import os  
import datetime

class SeverityLevel(Enum):
    info = 0
    warning = 1
    error = 2
    critical = 3

class ErrorMsg:
    #this class will be simmply a place where we define what we will log.
    DateStamp = ""  # time stamp of log
    ErrorMessage = ""  #actual Error message
    FileName = ""       #file name if we are dealing with a file
    Severity = ""       #this will be set to Info, Warning, Error, Critical.  this will be set by the enum class

    def setDateTime(self):
        thenow = datetime.datetime.now()
        self.DateStamp = thenow.strftime("%m/%d/%Y %H:%M:%S")

    def __init__(self):
        self.ErrorMessage = "init"



class LogFile:
    #this class will hold all the stuff with logging our issues out
    #for now, the methods will be very simple, and could in theory be combined into 1 call.  however
    # it is likely that in the future I will have to expand the functionality, and keeping these logical
    # activitiies seperateed will keep my life easy


    filehandle = ""

    ###### methods ##############
  
    def OpenLogFIle(self,logpath):
        #this will open the file in append mode, and set it to ready for writing.
        self.filehandle = open(logpath,"ab+")


    def CloseLogFile(self):
        #this will close the log file.
        self.filehandle.close()


    def WriteLogEntry(self,theerrormsg):
        #this will take the error msg object and write it to the log.
        root = ""
        xml = ""
        logxmlstr = ""

        root = minidom.Document() 
  
        xml = root.createElement('File2JsonLog')  
        root.appendChild(xml) 

        errorLineItem = root.createElement('Log') 
        errorLineItem.setAttribute('DateStamp',theerrormsg.DateStamp) 
        errorLineItem.setAttribute('ErrorMessage',theerrormsg.ErrorMessage) 
        errorLineItem.setAttribute('FileName',theerrormsg.FileName) 
        errorLineItem.setAttribute('Severity',theerrormsg.Severity)
        xml.appendChild(errorLineItem) 
  
        logxmlstr = root.toprettyxml(newl='\n',encoding="UTF-8") 
        #logxmlstr = str(root.toxml() )

        self.filehandle.write(logxmlstr)

    def __init__(self,logfilepath):
        #constructor.  this will go and open the file to have it ready for us to log to.
        self.OpenLogFIle(logfilepath)

