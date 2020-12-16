#!/usr/bin/python3
#kelly j  10-14-2020
#this will have the config file functionality.
#
#  we will read in teh config file, and set variables based on what we read in teh config file.
# the config file will be in xml
#kelly j  10-15-20  can't get reflection to work the way I wanted.  it seems that the losely typed nature of 
#           python won't allow this to happen easily, at least not the way I think it should.
#           what we have here will work, and for the most part is concise, while not easily changed.



from xml.dom.minidom import parse 
import xml.dom.minidom
import os
import inspect
import pprint

class ConfigFile:
    #this class will hold all the stuff we need for our config.  Our constructor will load the values in 

    source_directory = ""
    archive_directory = ""
    error_directory = ""
    complete_directory = ""
    logpath = ""
    format = ""
 
####### methods ###########################
    def AddTrailingSlash(self,path):
        if (not path.endswith("/") and not path.endswith("\\")):
            path+="/"

        return path

    def LoadConfigFile(self, configpath):
        #this will read in config file, and set our properties.
        #config file will be the that hsa the settings.
        try:
            cfgxml = xml.dom.minidom.parse(configpath)
            cfgParsed = cfgxml.documentElement

            AppElement = cfgParsed.getElementsByTagName('source_directory')[0]
            self.source_directory = self.AddTrailingSlash(AppElement.childNodes[0].data)


            AppElement = cfgParsed.getElementsByTagName('archive_directory')[0]
            self.archive_directory = self.AddTrailingSlash(AppElement.childNodes[0].data)

            AppElement = cfgParsed.getElementsByTagName('error_directory')[0]
            self.error_directory = self.AddTrailingSlash(AppElement.childNodes[0].data)

            AppElement = cfgParsed.getElementsByTagName('logpath')[0]
            self.logpath = AppElement.childNodes[0].data

            AppElement = cfgParsed.getElementsByTagName('complete_directory')[0]
            self.complete_directory = self.AddTrailingSlash(AppElement.childNodes[0].data)

            AppElement = cfgParsed.getElementsByTagName('format')[0]
            self.format = AppElement.childNodes[0].data


        except Exception as ex:
            print(ex)
        finally:
            pass
            # print("Config File Processed")
    
 
    def __init__(self,configpath):
        #constructor
        try:
            self.LoadConfigFile(configpath)

        except Exception as ex:
            print("Critical Error in Config File Constructor "+ex)









