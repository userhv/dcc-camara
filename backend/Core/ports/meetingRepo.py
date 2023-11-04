import sys
sys.path.insert(0,"..")
from Core.models.meeting import *
from abc import ABC, abstractmethod
class meetingRepository():

    @abstractmethod
    def getMeetingInfo(token:str,secretKey:str)->dict:
        pass
    @abstractmethod
    def createNewMeeting()->dict:
        pass
    @abstractmethod
    def insertDB(meeting:Meeting)-> str:
        pass
 