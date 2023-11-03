

from abc import ABC, abstractmethod
class userMeetingRepository():

    @abstractmethod
    def getUserMeetingInfo(userName:str,secretKey:str)->dict:
        pass

    @abstractmethod
    def createUserMeetingInfo(userId:str,meetingId:str)->dict:
        pass

   




        
