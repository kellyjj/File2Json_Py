#kelly j.  10-14-2020 File2Json
#
#this will be a tool that will take excel files, or delimited files and convert to either json
#or xml. Default will be json
#we will have a config file for all settings.  Logging for any thing that we need to track.
#the config functions will be in teh file ConfigFile.py.
#the logging functions will be in the LogFile.py file.

from ConfigFile import ConfigFile  #my config library
from LogFile    import LogFile      #my logging mechs
from LogFile    import ErrorMsg     #the error struct
from datetime   import date
from LogFile    import SeverityLevel
import datetime
import os
import re
import pandas as pn
import xlrd
import shutil
##### methods ######



#entry point

#load up our config.  only place with out a log
Cfg = ConfigFile("File2JsonConfig.xml")
Log = LogFile(Cfg.logpath)
TotalFilesProcessed = 0
TotalRecordsProcessed = 0
TotalErrors = 0

try:
    xlspattern = re.compile(r"\w+\.xl(s|sm|sx)")
    #we'll loop through the files, and process them indvidually.
 
    for thefiles in os.listdir(Cfg.source_directory):
        sumJson ="["

        try:
            print("Processing File "+str(TotalFilesProcessed))
            TotalFilesProcessed = TotalFilesProcessed+1
            if re.search(xlspattern,thefiles):
                allJsonStr = ""
                df = pn.read_excel(Cfg.source_directory+thefiles)
                for xlcnt in range(0,len(df)):
                    TotalRecordsProcessed = TotalRecordsProcessed +1
                    if (xlcnt % 500==0):
                        print("Processing row "+str(xlcnt),end="\r")
                    row = df.iloc[xlcnt]
                    allJsonStr+=row.to_json()+",\n"

                # allJsonStr = allJsonStr[:-1] 
                # allJsonStr +="]}"  
                sumJson+=allJsonStr
                print(" ")
                shutil.move(Cfg.source_directory+thefiles,Cfg.archive_directory+thefiles)
            else:
                #we have some other file
                print("Non excel file")

        except Exception as ex:
            FileErr = ErrorMsg()
            FileErr.setDateTime()
            FileErr.ErrorMessage = repr(ex)
            FileErr.FileName = "Unknown"
            FileErr.Severity = SeverityLevel(3).name
            Log.WriteLogEntry(FileErr)
            shutil.move(Cfg.source_directory+thefiles,Cfg.error_directory+thefiles)
            TotalErrors = TotalErrors +1

        sumJson =sumJson[:-2]
        sumJson+="]"
        theendTime = datetime.datetime.now()
        FinalFileName = Cfg.complete_directory+thefiles+"_"+theendTime.strftime("%m%d%Y%H%M")+".json"
        sumFileHandle = open(FinalFileName,"w+")
        sumFileHandle.write(sumJson)
        sumFileHandle.close()


except Exception as ex:
    MainErr = ErrorMsg()
    MainErr.setDateTime()
    MainErr.ErrorMessage = repr(ex)
    MainErr.FileName = "Unknown"
    MainErr.Severity = SeverityLevel(3).name
    Log.WriteLogEntry(MainErr)
    print(" ")
    print("Critical Error Processing Files -"+MainErr.ErrorMessage)

finally:
    SumErr = ErrorMsg()
    SumErr.setDateTime()
    SumErr.ErrorMessage = "Total Files Processed {0} Total Records Processed {1} Total Errors {2}".format(str(TotalFilesProcessed),str(TotalRecordsProcessed),str(TotalErrors))
    SumErr.FileName = "Unknown"
    SumErr.Severity = SeverityLevel(0).name
    Log.WriteLogEntry(SumErr)

    Log.CloseLogFile()
    print("\n\n---------------------------------------------------------------------------\n\n ")
    print(SumErr.ErrorMessage)
    print("Processing of Files Done")

#set up log.

#lets start the processing of the files.






