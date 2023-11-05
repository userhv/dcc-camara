
from abc import ABC, abstractmethod
class userRepository():

    @abstractmethod
    def getUserInfo(token:str,secretKey:str)->dict:
        pass
    @abstractmethod
    def loginUser(userName:str,secretKey:str)-> dict:
        pass
    
